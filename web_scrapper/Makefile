create_data_tests:
	python3 create_data_tests.py
	diff test_data.out test_data.out.correct

data.txt:
	cd ./skill_scores && python3 create_skill_scores.py
	cd ./weekly_data && python3 create_weekly_data.py
	python3 create_data.py

.PHONY: 
	create_skill_scores

clean:
	rm *.out *.txt