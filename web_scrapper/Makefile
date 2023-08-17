create_data_tests:
	python3 create_data_tests.py
	diff test_data.out test_data.out.correct

create_skill_scores:
	cd ./skill_scores && python3 create_skill_scores.py

.PHONY: 
	create_skill_scores

clean:
	rm *.out *.txt