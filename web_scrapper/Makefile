create_data_tests:
	cd ./skill_scores && python3 create_skill_scores_tests.py
	cd ./weekly_data && python3 create_weekly_data_tests.py
	cd ./rookie_seasons && python3 create_rookie_seasons_tests.py
	cd ./data && python3 create_data_tests.py
	cd ./team_id && python3 create_team_id_tests.py
	cd ./rookie_seasons && python3 create_rookie_seasons_tests.py
	diff create_data_tests.out create_data_tests.out.correct

data_tests:
	cd ./skill_scores && python3 create_skill_scores_tests.py
	cd ./weekly_data && python3 create_weekly_data_tests.py
	cd ./rookie_seasons && python3 create_rookie_seasons_tests.py
	cd ./team_id && python3 create_team_id_tests.py
	cd ./data && python3 create_data_tests.py	 

data.csv:
	cd ./skill_scores && python3 create_skill_scores.py
	cd ./weekly_data && python3 create_weekly_data.py
	cd ./rookie_seasons && python3 create_rookie_seasons.py
	cd ./team_id && python3 create_team_id.py
	cd ./data && python3 create_data.py


.PHONY: 

clean:
	 