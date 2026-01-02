# -*- coding: utf-8 -*-
"""
适用场景：
1. 无图形界面的 Linux 系统；
2. 使用 Selenium + Chromium Headless 模式；
3. 访问 https://zujuan.21cnjy.com 后自动登录；
4. 自动搜索关键词并解析题目与答案；
5. 输出结果保存到本地文件。
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import shutil
from bs4 import BeautifulSoup
import argparse
import requests
import base64
import os
import asyncio
import random
from urllib.parse import urljoin, urlparse
from openai import OpenAI
from volcenginesdkarkruntime import Ark, AsyncArk
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ 警告: PIL/Pillow未安装，无法调整图片尺寸。请运行: pip install Pillow")


# ===== 用户配置 =====
URL = "https://zujuan.21cnjy.com/question?tree_type=knowledge&xd=3&chid=3"
USERNAME = "18192300180"         # 你的登录账号
PASSWORD = "xx100806"           # 你的密码
KEYWORD = "幂函数"    # 搜索关键词
OUTPUT_FILE = "题目_答案.txt"
WAIT_TIME = 3                 # 页面加载等待时间（秒）
IMAGES_DIR = "math_images"    # 图片保存目录
DOUBAO_API_KEY = "196b33be-8abb-4af3-9fba-6e266b2dd942"  # 豆包API密钥

# ===== 初始化 Headless Chrome =====
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # 自动寻找 Chromium 与 chromedriver
    CHROME_PATH = shutil.which("chromium-browser") or shutil.which("google-chrome")
    CHROMEDRIVER_PATH = shutil.which("chromedriver") or "/usr/bin/chromedriver"
    service = Service(CHROMEDRIVER_PATH)
    return webdriver.Chrome(service=service, options=chrome_options)

def wait_visible(driver, by, selector, timeout=10):
    """等待元素显示"""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))


# ===== Vision API 相关函数 =====
async def recognize_math_image_async(image_path):
    """
    使用豆包Vision API异步识别图片中的数学公式
    :param image_path: 图片路径（绝对路径）
    :return: 识别出的数学公式文本（LaTeX格式）
    """
    try:
        # 转换为绝对路径
        abs_image_path = os.path.abspath(image_path)
        
        # 创建异步客户端
        async_client = AsyncArk(
            base_url='https://ark.cn-beijing.volces.com/api/v3',
            api_key=DOUBAO_API_KEY
        )
        
        # 调用豆包Vision API
        response = await async_client.responses.create(
            model="doubao-seed-1-6-251015",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_image",
                            "image_url": f"file://{abs_image_path}"
                        },
                        {
                            "type": "input_text",
                            "text": "请识别这张图片中的数学公式，使用LaTeX格式输出。只输出图中公式内容，不要有任何其他内容。"
                        }
                    ]
                }
            ]
        )
        
        # 提取识别结果（根据实际响应结构）
        try:
            formula = None
            
            # 尝试 responses.create 的响应结构：response.output 是一个列表
            if hasattr(response, 'output') and response.output:
                # output 是一个列表，找到 ResponseOutputMessage 类型的项
                for item in response.output:
                    # 检查是否是消息类型
                    if hasattr(item, 'type') and item.type == 'message':
                        if hasattr(item, 'content') and item.content:
                            # content 也是一个列表，找到 ResponseOutputText 类型的项
                            for content_item in item.content:
                                if hasattr(content_item, 'type') and content_item.type == 'output_text':
                                    if hasattr(content_item, 'text'):
                                        formula = content_item.text
                                        break
                            if formula:
                                break
                    # 如果找不到message类型，尝试直接访问text属性
                    if not formula and hasattr(item, 'text'):
                        formula = item.text
                        break
            
            if not formula:
                formula = "[未能提取到文本内容]"
            else:
                formula = formula.strip()
                
        except (AttributeError, IndexError, TypeError) as e:
            print(f"⚠️ 解析响应结构失败: {e}")
            print(f"   响应类型: {type(response)}")
            if hasattr(response, 'output'):
                print(f"   output类型: {type(response.output)}")
            formula = f"[响应解析失败]"
        
        # 清理可能的markdown代码块标记
        formula = formula.replace('```latex', '').replace('```', '').strip()
        return formula
    except Exception as e:
        print(f"⚠️ 识别图片失败 {image_path}: {e}")
        return f"[公式识别失败]"


def resize_image_if_needed(image_path, min_dimension=16):
    """
    检查图片尺寸，如果宽或高小于最小尺寸要求，则放大图片
    :param image_path: 图片路径
    :param min_dimension: 最小尺寸（像素），默认16（API要求14，留一些余量）
    :return: 是否需要调整（True表示已调整，False表示不需要调整）
    """
    if not PIL_AVAILABLE:
        print("⚠️ 无法调整图片尺寸: PIL/Pillow未安装")
        return False
    
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            print(f"  📏 图片尺寸: {width}x{height}")
            
            # 检查是否需要调整
            if width >= min_dimension and height >= min_dimension:
                return False  # 不需要调整
            
            # 计算缩放比例，确保两个维度都至少达到最小尺寸
            scale_w = min_dimension / width if width < min_dimension else 1
            scale_h = min_dimension / height if height < min_dimension else 1
            scale = max(scale_w, scale_h)
            
            # 计算新尺寸（向上取整，确保至少达到最小尺寸）
            new_width = max(int(width * scale), min_dimension)
            new_height = max(int(height * scale), min_dimension)
            
            # 使用高质量重采样算法（兼容新旧版本Pillow）
            try:
                # 新版本Pillow使用Image.Resampling.LANCZOS
                resample = Image.Resampling.LANCZOS
            except AttributeError:
                # 旧版本使用Image.LANCZOS
                resample = Image.LANCZOS
            
            resized_img = img.resize((new_width, new_height), resample)
            
            # 保存调整后的图片（覆盖原文件）
            resized_img.save(image_path, 'PNG')
            print(f"  📏 图片尺寸调整: {width}x{height} -> {new_width}x{new_height}")
            return True
    except Exception as e:
        print(f"⚠️ 调整图片尺寸失败 {image_path}: {e}")
        return False


def download_image(img_url, img_path, session=None, driver=None):
    """
    下载图片到本地，支持SVG格式并自动转换为PNG
    :param img_url: 图片URL（可能是相对路径或绝对路径）
    :param img_path: 保存路径（应该以.png结尾）
    :param session: requests session对象（用于保持cookies）
    :param driver: Selenium driver对象（用于SVG截图）
    :return: 是否下载成功
    """
    try:
        # 处理协议相对URL（以//开头）
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        # 如果是相对路径，转换为绝对路径
        elif not img_url.startswith('http'):
            img_url = urljoin(URL, img_url)
        
        # 确保目录存在
        img_dir = os.path.dirname(img_path)
        if img_dir:
            os.makedirs(img_dir, exist_ok=True)
        
        # 检查URL是否指向SVG（mml2svg表示SVG格式）
        is_svg_url = 'mml2svg' in img_url or 'svg' in img_url.lower()
        
        # 下载内容
        if session:
            response = session.get(img_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        else:
            response = requests.get(img_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        # 检查内容类型和内容，判断是否为SVG
        content_type = response.headers.get('Content-Type', '').lower()
        content_preview = response.content[:200] if len(response.content) > 0 else b''
        
        is_svg = is_svg_url or 'svg' in content_type
        if not is_svg:
            try:
                content_str = content_preview.decode('utf-8', errors='ignore')
                is_svg = content_str.strip().startswith('<?xml') or content_str.strip().startswith('<svg')
            except:
                pass
        
        # 如果是SVG格式，使用selenium截图转换为PNG
        if is_svg and driver:
            try:
                # 使用selenium访问SVG URL并截图
                driver.get(img_url)
                time.sleep(0.5)  # 等待SVG加载
                svg_element = driver.find_element(By.TAG_NAME, 'svg')
                svg_element.screenshot(img_path)
                print(f"  ✅ SVG已转换为PNG: {img_path}")
                return True
            except Exception as e:
                print(f"⚠️ SVG截图失败: {e}")
                # 如果截图失败，尝试保存原始SVG内容
                try:
                    svg_path = img_path.replace('.png', '.svg')
                    with open(svg_path, 'wb') as f:
                        f.write(response.content)
                    print(f"⚠️ 已保存为SVG文件: {svg_path}")
                except:
                    pass
                return False
        elif is_svg:
            print(f"⚠️ 检测到SVG格式，但driver未提供，无法转换")
            # 保存为SVG文件
            svg_path = img_path.replace('.png', '.svg')
            with open(svg_path, 'wb') as f:
                f.write(response.content)
            print(f"⚠️ 已保存为SVG文件: {svg_path}")
            return False
        else:
            # 非SVG格式，直接保存
            with open(img_path, 'wb') as f:
                f.write(response.content)
            return True
            
    except Exception as e:
        print(f"⚠️ 下载图片失败 {img_url}: {e}")
        return False

def extract_option_content(op_item_element, driver, session, question_idx, option_idx):
    """
    提取选项内容（可能是文本或图片）
    :param op_item_element: 选项元素 (span.op-item)
    :param driver: Selenium driver
    :param session: requests session
    :param question_idx: 题目索引
    :param option_idx: 选项索引 (0=A, 1=B, 2=C, 3=D)
    :return: 选项内容的文本表示
    """
    option_letter = ['A', 'B', 'C', 'D'][option_idx]
    
    # 查找选项内容部分 (span.op-item-meat)
    meat_span = op_item_element.find('span', class_='op-item-meat')
    if not meat_span:
        return ""
    
    # 检查是否有图片
    img_tags = meat_span.find_all('img', class_='mathml')
    if img_tags:
        # 有图片，需要识别
        option_text = ""
        for img_idx, img in enumerate(img_tags):
            img_src = img.get('src', '')
            if not img_src:
                continue
            
            # 构建图片保存路径
            img_filename = f"q{question_idx}_opt{option_letter}_img{img_idx}.png"
            img_path = os.path.join(IMAGES_DIR, img_filename)
            abs_img_path = os.path.abspath(img_path)
            
            # 下载图片
            if download_image(img_src, abs_img_path, session, driver):
                # 预处理图片
                resize_image_if_needed(abs_img_path, min_dimension=16)
                
                # 识别图片
                loop = asyncio.get_event_loop()
                formula = loop.run_until_complete(recognize_math_image_async(abs_img_path))       
                option_text += formula
            else:
                option_text += "[图片下载失败]"
        return option_text.strip()
    else:
        # 没有图片，直接返回文本
        return meat_span.get_text(strip=True)


def extract_answer_with_options(question_element, driver, session, question_idx):
    """
    提取选择题的选项和答案
    :param question_element: 题目元素
    :param driver: Selenium driver
    :param session: requests session
    :param question_idx: 题目索引
    :return: (选项字典{A:内容, B:内容, ...}, 答案内容)
    """
    options = {}
    answer_content = ""
    
    # 查找选项容器 - 根据图2，选项在 span.op-item 中
    question_block = question_element.find_parent('div', class_='question-block')
    if question_block:
        # 查找所有选项 (span.op-item)
        op_items = question_block.find_all('span', class_='op-item')
        
        if op_items:
            # 提取每个选项的内容
            for idx, op_item in enumerate(op_items[:4]):  # 最多4个选项
                option_letter = ['A', 'B', 'C', 'D'][idx]
                option_content = extract_option_content(op_item, driver, session, question_idx, idx)
                if option_content:  # 只添加非空选项
                    options[option_letter] = option_content
                    print(f"  选项{option_letter}: {option_content}")
    
    # 查找答案部分 - 根据图3，答案在 div.q-analyize-mc 中
    analyze_div = question_element.find_next('div', class_='q-analyize')

    if analyze_div:
        print(f"  📥 找到答案部分: {analyze_div}") 
        # 查找答案部分 - 先找 J_ana_ans 容器
        ans_item = analyze_div.find('div', class_='J_ana_ans')
        if ans_item:
            # 查找答案内容 (div.q-analyize-mc)
            ans_mc = ans_item.find('div', class_='q-analyize-mc')
            if ans_mc:
                # 检查答案中是否有图片
                img_tags = ans_mc.find_all('img')
                if img_tags:
                    # 有图片，需要识别
                    for img_idx, img in enumerate(img_tags):
                        img_src = img.get('src', '')
                        if not img_src:
                            continue
                        
                        img_filename = f"q{question_idx}_ans_img{img_idx}.png"
                        print(f"  📥 下载答案图片: {img_filename}")
                        img_path = os.path.join(IMAGES_DIR, img_filename)
                        abs_img_path = os.path.abspath(img_path)
                        
                        if download_image(img_src, abs_img_path, session, driver):
                            resize_image_if_needed(abs_img_path, min_dimension=16)
                            loop = asyncio.get_event_loop()
                            formula = loop.run_until_complete(recognize_math_image_async(abs_img_path))
                            answer_content += formula
                        else:
                            answer_content += "[图片下载失败]"
                else:
                    # 没有图片，直接获取文本
                    answer_content = ans_mc.get_text(strip=True)
                
                # 清理答案内容
                answer_content = answer_content.strip()
                
                # 如果答案是选项标记（如"D"），查找对应的选项内容
                if answer_content in options:
                    answer_mark = answer_content  # 保存原始标记
                    answer_content = options[answer_content]
                    print(f"  答案标记{answer_mark}对应内容: {answer_content}")
    
    return options, answer_content


def extract_and_replace_images(soup_element, driver, session, question_idx):
    """
    提取元素中的图片，识别后替换为LaTeX公式
    """
    # 创建元素的副本以避免修改原始元素
    element_copy = BeautifulSoup(str(soup_element), 'lxml').find()
    
    # 查找所有mathml图片
    img_tags = element_copy.find_all('img', class_='mathml')
    
    # 如果没有图片，直接返回文本
    if not img_tags:
        return element_copy.get_text(strip=True)
    
    # 创建文本替换映射
    replacements = []
    
    for img_idx, img in enumerate(img_tags):
        img_src = img.get('src', '')
        if not img_src:
            continue
        
        # 构建图片保存路径（使用绝对路径）
        img_filename = f"q{question_idx}_img{img_idx}.png"
        img_path = os.path.join(IMAGES_DIR, img_filename)
        abs_img_path = os.path.abspath(img_path)
        
        # 下载图片
        print(f"  📥 下载图片 {img_idx + 1}/{len(img_tags)}: {img_filename}")
        if download_image(img_src, abs_img_path, session, driver):

            # 预处理图片：检查并调整尺寸（确保满足API最小尺寸要求）
            resize_image_if_needed(abs_img_path, min_dimension=16)
            
            # 识别图片（使用异步API，通过同步包装器调用）
            print(f"  🔍 识别图片: {img_filename}")
            loop = asyncio.get_event_loop()
            formula = loop.run_until_complete(recognize_math_image_async(abs_img_path))
            print(f"  ✅ 识别结果: {formula}")
            
            # 记录替换映射（使用唯一占位符）
            placeholder = f"__MATH_FORMULA_{img_idx}__"
            img.replace_with(placeholder)
            replacements.append((placeholder, formula))
        else:
            # 下载失败，使用占位符
            placeholder = f"__MATH_FORMULA_{img_idx}__"
            img.replace_with(placeholder)
            replacements.append((placeholder, "[图片下载失败]"))
    
    # 获取替换后的文本
    result_text = element_copy.get_text(separator=' ', strip=False)
    
    # 执行替换
    for placeholder, formula in replacements:
        result_text = result_text.replace(placeholder, f"${formula}$")
    
    return result_text


# ===== 登录函数 =====
def login(driver):
    print("🔐 正在打开登录页面...")
    driver.get("https://passport.21cnjy.com/login?jump_url=https://zujuan.21cnjy.com/u/index")

    # 等待登录页加载完成
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".login-tabs"))
    )
    time.sleep(1)

    # ✅ 点击“账号密码登录”选项卡（data-type="pwd"）
    try:
        print("🧭 切换到【账号密码登录】模式...")
        pwd_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-type='pwd']"))
        )
        driver.execute_script("arguments[0].click();", pwd_tab)
        time.sleep(1.5)  # 等待动画或 DOM 切换完成
    except Exception as e:
        print(f"⚠️ 无法切换至账号密码登录模式：{e}")

    # 等待账号输入框变为可见
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, "user-pwd"))
    )

    print("➡️  输入账号和密码...")
    username_input = driver.find_element(By.ID, "user-name")
    password_input = driver.find_element(By.ID, "user-pwd")

    username_input.clear()
    username_input.send_keys(USERNAME)
    time.sleep(0.5)
    password_input.clear()
    password_input.send_keys(PASSWORD)
    time.sleep(0.5)

    # 点击登录按钮
    print("🚪 正在点击登录按钮...")
    login_btn = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-submit")
    driver.execute_script("arguments[0].click();", login_btn)

    # 验证是否成功
    try:
        # 等待URL跳转到 zujuan.21cnjy.com 域名（登录成功后会跳转）
        WebDriverWait(driver, 20).until(
            lambda d: "zujuan.21cnjy.com" in d.current_url
        )
        print("✅ 登录成功，正在跳转...")
    except Exception:
        print("⚠️ 登录失败，请检查账号或验证码！")

    time.sleep(2)


# ===== 搜索并抓取题目 =====
def scrape_questions(driver, keyword, output_file):
    print(f"🔍 正在访问：{URL}")
    driver.get(URL)

    # 等待页面加载完成，特别是左侧知识树区域
    time.sleep(WAIT_TIME)
    
    # 等待左侧搜索框出现（根据HTML结构：form#J_ltsrchFrm > input[name='know_txt']）
    print("🔍 正在定位搜索框...")
    search_box = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='know_txt'], #J_ltsrchFrm input[type='text'], .fm-txt"))
    )

    print(f"📝 在搜索框中输入关键词: {keyword}")
    search_box.clear()
    search_box.send_keys(keyword)
    time.sleep(1)
    search_box.send_keys(Keys.ENTER)  
    time.sleep(WAIT_TIME + 2)

    # 点击左侧对应知识点
    try:
        print(f"➡️  正在查找菜单项【{keyword}】...")
        # 等待搜索结果出现（搜索结果通常在 .list-tree-search-list 或 .list-ts-chbox 区域）
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".list-ts-item, .J_ListTsItem"))
        )
        time.sleep(1)  # 额外等待搜索结果渲染

        link = None
        
        # 策略1: 尝试精确匹配（去除<em>标签后文本完全匹配）
        try:
            # 查找所有匹配的条目
            all_matches = driver.find_elements(By.XPATH, f"//span[@class='ts-tit' and contains(., '{keyword}')]/ancestor::li[contains(@class, 'list-ts-item')]")
            if all_matches:
                # 遍历所有匹配项，查找文本完全匹配的
                for item in all_matches:
                    text_content = item.find_element(By.CSS_SELECTOR, "span.ts-tit").text.strip()
                    # 去除可能的空格和特殊字符后比较
                    if text_content == keyword or text_content.replace(' ', '') == keyword.replace(' ', ''):
                        link = item
                        print(f"✅ 找到精确匹配: {text_content}")
                        break
                
                # 如果没有精确匹配，选择第一个
                if link is None:
                    link = all_matches[0]
                    text_content = link.find_element(By.CSS_SELECTOR, "span.ts-tit").text.strip()
                    print(f"⚠️  未找到精确匹配，选择第一个匹配项: {text_content}")
        except Exception as e:
            print(f"⚠️ 匹配过程中出现错误: {e}")

        if link is None:
            raise Exception("未找到匹配的知识点条目")
        
        # 滚动元素到可视区域（这是关键步骤，避免element not interactable错误）
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", link)
        time.sleep(0.5)
        
        # 确保元素可见
        driver.execute_script("arguments[0].style.display = 'block';", link)
        WebDriverWait(driver, 10).until(
            EC.visibility_of(link)
        )
        
        # 使用JavaScript点击，更可靠（避免element not interactable错误）
        # JavaScript click 可以绕过许多交互性问题
        driver.execute_script("arguments[0].click();", link)
        print(f"✅ 成功点击知识点: {keyword}")
        time.sleep(WAIT_TIME + 2)
    except Exception as e:
        print(f"⚠️ 未找到左侧菜单【{keyword}】，错误信息: {e}")
        print(f"⚠️ 将直接解析当前页面内容。")

    # 创建requests session以保持cookies（用于下载图片）
    print("🔧 初始化下载会话...")
    session = requests.Session()
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])
    
    # 确保图片目录存在
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    # 解析题目内容
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    questions = soup.select("ul li div.q-tit")
    results = []

    print(f"🧐 共发现 {len(questions)} 道题。")
    
    # 随机选择一道题
    if len(questions) == 0:
        print("⚠️ 未找到任何题目")
        return
    
    selected_idx = random.randint(0, len(questions) - 1)
    selected_q = questions[selected_idx]
    actual_idx = selected_idx + 1  # 题目编号从1开始
    
    print(f"🎲 随机选择第 {actual_idx} 题进行处理...")
    
    # 提取题目文本，并识别其中的数学公式图片
    q_text = extract_and_replace_images(selected_q, driver, session, actual_idx)
    q_text = q_text.replace(" ", "")

    # 提取选项和答案
    print(f"\n📋 提取选项和答案...")
    options, answer_content = extract_answer_with_options(selected_q, driver, session, actual_idx)
    
    # 如果找到了选项，说明是选择题
    if options:
        # 构建答案文本
        if answer_content:
            ans_text = answer_content
        else:
            ans_text = "（未找到答案内容）"
        
        results.append(f"{q_text}\n答案：{ans_text}\n")
    else:
        # 不是选择题，使用原来的方法提取答案
        ans_div = selected_q.find_next("div", class_="q-analyze")
        if ans_div:
            ans_text = extract_and_replace_images(ans_div, driver, session, f"{actual_idx}_ans")
            ans_text = ans_text.replace(" ", "")
        else:
            ans_text = "（未找到答案）"
        
        results.append(f"{q_text}\n答案：{ans_text}\n")
    
    # 保存结果
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))

    print(f"\n✅ 已保存相关题目至文件：{output_file}")


# ===== 主程序入口 =====
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="自动登录并抓取题目")
    parser.add_argument("--keyword", type=str, default=KEYWORD, help="搜索关键词")
    parser.add_argument("--output", type=str, default=OUTPUT_FILE, help="输出文件")
    args = parser.parse_args()

    print("🚀 启动 Headless 浏览器...")
    driver = init_driver()
    try:
        login(driver)
        scrape_questions(driver, args.keyword, args.output)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
    finally:
        driver.quit()
        print("🛑 浏览器已关闭。")