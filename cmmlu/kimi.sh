python test_language_dir.py --dir=./test_japanese --model=kimi --language=japanese > log/test_japanese_kimi.log
python test_language_dir.py --dir=./test_arabic --model=kimi --language=arabic > log/test_arabic_kimi.log
python test_language_dir.py --dir=./test_english --model=kimi --language=english > log/test_english_kimi.log
python test_origin_dir.py --dir=./test --model=kimi > log/test_origin_kimi.log
python test_few_shot_dir.py --dir=./test --dir_few_shot=./dev --model=kimi > log/test_few_shot_kimi.log
python test_cot_dir.py --dir=./test --model=kimi > log/test_cot_kimi.log