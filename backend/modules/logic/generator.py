from ortools.linear_solver import pywraplp
from random import randint
import random


def filter_question_answers(question, displayed_answers):
    answers = question['body']
    correct_answers = 0
    filtered_answers = []
    not_chosen = []
    for answer in answers:
        if answer['mandatory'] == 1:
            if answer['correction'] == 1:
                correct_answers += 1
            filtered_answers.append(answer)
        else:
            not_chosen.append(answer)

    if correct_answers == 0:
        correct = list(
            filter(lambda elem: elem['correction'] == 1, not_chosen))
        if len(correct) == 0:
            # Data is malformed, the question does not have a correct option
            return
        else:
            filtered_answers.append(correct[0])
            not_chosen.remove(correct[0])
    else:
        not_chosen = list(
            filter(lambda elem: elem['correction'] == 0, not_chosen))

    if len(filtered_answers) < displayed_answers:
        left_to_choose = min(
            len(not_chosen), displayed_answers - len(filtered_answers))
        leftover = random.sample(
            range(1, len(filtered_answers) - 1), left_to_choose)
        for idx in leftover:
            filtered_answers.append(not_chosen[idx])
    question['body'] = filtered_answers
    return


def generate_test(question_pool, num_questions, displayed_answers, total_time, average_difficulty):
    print('numq - ' +str(num_questions) +  ', disans -' + str(displayed_answers) + ', tots -' + str(total_time) + ', avg  ' + str(average_difficulty) )
    solver = pywraplp.Solver.CreateSolver('SCIP')

    nr_tolerance = int(0.4 * num_questions)
    difficulty_tolerance = float(0.4 * average_difficulty)

    lower_nr_bound = num_questions - nr_tolerance
    upper_nr_bound = num_questions + nr_tolerance

    lower_difficulty_bound = (
        average_difficulty - difficulty_tolerance) * num_questions
    upper_difficulty_bound = (
        average_difficulty + difficulty_tolerance) * num_questions

    variables = []
    ids = []
    times = []
    difficulties = []
    weights = []
    counter = 0

    print('Generating Test...')
    print('Request Avg Difficulty:' + str(average_difficulty))
    print('Question Pool Length: ' + str(len(question_pool)))
    avg_dif = sum(
        list(map(lambda q: int(q['difficulty_level']), question_pool))) / len(question_pool)
    print('Average Difficulty of the question pool: ' + str(avg_dif))
    q_diffs = list(map(lambda q: q['difficulty_level'], question_pool))
    print(q_diffs)
    for q in question_pool:
        variables.append(solver.IntVar(0.0, 1.0, 'var[%i]' % counter))
        counter += 1
        ids.append(q['_id'])
        print(q['_id'] + ' -----')
        times.append(float(q['answering_time']))
        difficulties.append(float(q['difficulty_level']))
        weights.append(randint(1, 100))
    number_questions_constraints = solver.RowConstraint(
        num_questions, num_questions)
    time_sum_constraint = solver.RowConstraint(
        0, total_time)
    average_difficulty_constraint = solver.RowConstraint(
        average_difficulty * num_questions, average_difficulty * num_questions)
    objective = solver.Objective()

    for i in range(0, len(variables)):
        number_questions_constraints.SetCoefficient(variables[i], 1)
        time_sum_constraint.SetCoefficient(variables[i], times[i])
        average_difficulty_constraint.SetCoefficient(
            variables[i], difficulties[i])
        objective.SetCoefficient(variables[i], weights[i])

    max_or_min = randint(0, 1)
    if max_or_min == 0:
        objective.SetMaximization()
    else:
        objective.SetMinimization()

    status = solver.Solve()
    print('status --  ' + str(status))

    print(pywraplp.Solver.OPTIMAL)

    print(pywraplp.Solver.FEASIBLE)
    result = []
    if status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
        print("Exact result found")
        for i in range(0, len(variables)):
            if variables[i].solution_value():
                filter_question_answers(
                    question_pool[i], displayed_answers)
                result.append(question_pool[i])
    else:
        print("No exact result found, attempting with 20% tolerance")
        number_questions_constraints.SetBounds(lower_nr_bound, upper_nr_bound)
        time_sum_constraint.SetBounds(0, total_time)
        average_difficulty_constraint.SetBounds(
            lower_difficulty_bound, upper_difficulty_bound)
        status = solver.Solve()

        print('status --  ' + str(status))
        if status in [pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE]:
            for i in range(0, len(variables)):
                if variables[i].solution_value():
                    filter_question_answers(
                        question_pool[i], displayed_answers)
                    result.append(question_pool[i])
    return result
