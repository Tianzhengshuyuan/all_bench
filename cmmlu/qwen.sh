python test_language_dir.py --dir=./test_japanese --model=qwen --language=japanese > log/test_japanese_qwen.log
python test_language_dir.py --dir=./test_arabic --model=qwen --language=arabic > log/test_arabic_qwen.log
python test_language_dir.py --dir=./test_english --model=qwen --language=english > log/test_english_qwen.log
python test_origin_dir.py --dir=./test --model=qwen > log/test_origin_qwen.log
python test_few_shot_dir.py --dir=./test --dir_few_shot=./dev --model=qwen > log/test_few_shot_qwen.log
python test_cot_dir.py --dir=./test --model=qwen > log/test_cot_qwen.log