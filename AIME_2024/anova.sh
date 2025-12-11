# echo "mistralL"
# python get_main_anova.py --logfile log/sample_test_mistralL.log --pkl_path sample_data_v1.2.pkl --sample_num=500 --interaction --merge_language > anova_linear_result/mistralL.log
# echo "mistralM"
# python get_main_anova.py --logfile log/sample_test_mistralM.log --pkl_path sample_data_v1.2.pkl --sample_num=500 --interaction --merge_language > anova_linear_result/mistralM.log
# echo "deepseek"
# python get_main_anova.py --logfile log/sample_test_deepseekv3.log --pkl_path sample_data_v1.2.pkl --sample_num=500 --interaction --merge_language > anova_linear_result/deepseek.log
# echo "doubao"
# python get_main_anova.py --logfile log/sample_test_doubao.log --pkl_path sample_data_v1.2.pkl --sample_num=500 --interaction --merge_language > anova_linear_result/doubao.log
# echo "kimiv1"
# python get_main_anova.py --logfile log/sample_test_kimiv1.log --pkl_path sample_data_v1.2.pkl --sample_num=500 --interaction --merge_language > anova_linear_result/kimiv1.log
# echo "qwen"
# python get_main_anova.py --logfile log/sample_test_qwen.log --pkl_path sample_data_v1.2.pkl --sample_num=500 --interaction --merge_language > anova_linear_result/qwen.log
# echo "qwen25"
# python get_main_anova.py --logfile log/sample_test_qwen25.log --pkl_path sample_data_v1.2.pkl --sample_num=500 --interaction --merge_language > anova_linear_result/qwen25.log
# echo "gpt35"
# python get_main_anova.py --logfile log/sample_test_gpt35.log --pkl_path sample_data_v1.2.pkl --sample_num=500 --interaction --merge_language > anova_linear_result/gpt35.log
# echo "gpt41"
# python get_main_anova.py --logfile log/sample_test_gpt41.log --pkl_path sample_data_v1.2.pkl --sample_num=500 --interaction --merge_language > anova_linear_result/gpt41.log
python get_main_anova_dir.py --label doubao --interaction > anova_1024_result/doubao.log
python get_main_anova_dir.py --label deepseekv3 --interaction > anova_1024_result/deepsek.log
python get_main_anova_dir.py --label kimiv1 --interaction > anova_1024_result/kimi.log
python get_main_anova_dir.py --label qwen25 --interaction > anova_1024_result/qwen25.log
python get_main_anova_dir.py --label mistralM --interaction > anova_1024_result/mistralM.log