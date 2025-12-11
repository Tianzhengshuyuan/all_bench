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

# ===== 用户配置 =====
URL = "https://zujuan.21cnjy.com/question?tree_type=knowledge&xd=2&chid=3"
USERNAME = "18192300180"         # 你的登录账号
PASSWORD = "xx100806"           # 你的密码
KEYWORD = "方程的定义及分类"    # 搜索关键词
OUTPUT_FILE = "题目_答案.txt"
WAIT_TIME = 3                 # 页面加载等待时间（秒）

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

    print("➡️ 输入账号和密码...")
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
        WebDriverWait(driver, 20).until_not(
            EC.url_contains("passport.21cnjy.com")
        )
        print("✅ 登录成功，正在跳转...")
    except Exception:
        print("⚠️ 登录失败，请检查账号或验证码！")

    time.sleep(2)


# ===== 搜索并抓取题目 =====
def scrape_questions(driver, keyword, output_file):
    print(f"🔍 正在访问：{URL}")
    driver.get(URL)

    # 等待搜索框出现
    search_box = wait_visible(driver, By.CSS_SELECTOR, "input[type='text']")
    time.sleep(WAIT_TIME)

    search_box.clear()
    search_box.send_keys(keyword)
    time.sleep(1)
    search_box.send_keys(Keys.ENTER)
    time.sleep(WAIT_TIME + 2)

    # 点击左侧对应知识点
    try:
        print(f"➡️ 正在查找菜单项【{keyword}】...")
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{keyword}')]"))
        )
        driver.execute_script("arguments[0].click();", link)
        time.sleep(WAIT_TIME + 2)
    except Exception:
        print(f"⚠️ 未找到左侧菜单【{keyword}】，将直接解析当前页面内容。")

    # 解析题目内容
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    questions = soup.select("ul li div.q-tit")
    results = []

    print(f"🧐 共发现 {len(questions)} 道题。")

    for idx, q in enumerate(questions, start=1):
        q_text = q.get_text(strip=True)
        ans_div = q.find_next("div", class_="q-analyze")
        ans_text = ans_div.get_text(strip=True) if ans_div else "（未找到答案）"
        results.append(f"{idx}. 题目：{q_text}\n答案：{ans_text}\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(results))

    print(f"✅ 已保存 {len(results)} 道题至文件：{output_file}")


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