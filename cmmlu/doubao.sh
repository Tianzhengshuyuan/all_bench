python test_few_shot_dir.py --dir=./test --dir_few_shot=./dev --model=doubao > log/test_few_shot_doubao.log
python test_cot_dir.py --dir=./test --model=doubao > log/test_cot_doubao.log 
python test_multi_turn.py --dir=./test --model=doubao > log/test_multi_turn_doubao.log