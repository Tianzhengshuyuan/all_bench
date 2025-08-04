python test_few_shot_dir.py --dir=./test --dir_few_shot=./dev --model=qwen > log/test_few_shot_qwen.log
python test_cot_dir.py --dir=./test --model=qwen > log/test_cot_qwen.log 
python test_multi_turn.py --dir=./test --model=qwen > log/test_multi_turn_qwen.log