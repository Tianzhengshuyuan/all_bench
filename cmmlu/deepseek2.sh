# python test_origin_dir.py --dir=./test --model=deepseek --max_tokens=10 > log/test_deepseek_m10.log
# echo "deepseek m10测试完成"
# python test_origin_dir.py --dir=./test --model=deepseek --max_tokens=50 > log/test_deepseek_m50.log
# echo "deepseek m50测试完成"
# python test_origin_dir.py --dir=./test --model=deepseek --max_tokens=100 > log/test_deepseek_m100.log
# echo "deepseek m100测试完成"
# python test_cot_dir.py --dir=./test --model=deepseek > log/test_cot_deepseek.log
# echo "deepseek cot 测试完成"
python test_origin_dir.py --dir=./test --model=deepseek --top_p=1.0 > log/test_deepseek_p1.0.log
echo "deepseek p1.0 测试完成"