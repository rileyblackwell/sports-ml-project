create_data_tests:
	cd ./skill_scores && python3 create_skill_scores_tests.py
	cd ./weekly_data && python3 create_weekly_data_tests.py
	cd ./rookie_seasons && python3 create_rookie_seasons_tests.py
	python3 create_data_tests.py
	diff create_data_tests.out create_data_tests.out.correct

data.txt:
	cd ./skill_scores && python3 create_skill_scores.py
	cd ./weekly_data && python3 create_weekly_data.py
	cd ./rookie_seasons && python3 create_rookie_seasons.py
	python3 create_data.py

.PHONY: 
	create_skill_scores

clean:
	rm *.out *.txt