python test_language_dir.py --dir=./test_japanese --model=doubao --language=japanese > log/test_japanese_doubao.log
python test_language_dir.py --dir=./test_arabic --model=doubao --language=arabic > log/test_arabic_doubao.log
python test_language_dir.py --dir=./test_english --model=doubao --language=english > log/test_english_doubao.log
python test_origin_dir.py --dir=./test --model=doubao > log/test_origin_doubao.log
python test_few_shot_dir.py --dir=./test --dir_few_shot=./dev --model=doubao > log/test_few_shot_doubao.log
python test_cot_dir.py --dir=./test --model=doubao > log/test_cot_doubao.log