python test_language_dir.py --dir=./test_japanese --model=deepseek --language=japanese > log/test_japanese_deepseek.log
python test_language_dir.py --dir=./test_arabic --model=deepseek --language=arabic > log/test_arabic_deepseek.log
python test_language_dir.py --dir=./test_english --model=deepseek --language=english > log/test_english_deepseek.log
python test_origin_dir.py --dir=./test --model=deepseek > log/test_origin_deepseek.log
python test_few_shot_dir.py --dir=./test --dir_few_shot=./dev --model=deepseek > log/test_few_shot_deepseek.log
python test_cot_dir.py --dir=./test --model=deepseek > log/test_cot_deepseek.log