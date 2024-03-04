
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append("hi,welcome")

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.

    '''
    if not answer:
        return False, "Please provide a valid answer."
    session["answers"].append({"question_id": current_question_id, "answer": answer})
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    for index, question in enumerate(PYTHON_QUESTION_LIST):
        if question["id"] == current_question_id:
            if index + 1 < len(PYTHON_QUESTION_LIST):
                next_question = PYTHON_QUESTION_LIST[index + 1]["question"]
                next_question_id = PYTHON_QUESTION_LIST[index + 1]["id"]
                return next_question, next_question_id

    return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    total_questions = len(PYTHON_QUESTION_LIST)
    user_answers = session.get("answers", [])

    
    correct_answers = 0
    for user_answer in user_answers:
        question_id = user_answer["question_id"]
        answer = user_answer["answer"]

        
        correct_answer = next(q["correct_answer"] for q in PYTHON_QUESTION_LIST if q["id"] == question_id)

        
        if answer == correct_answer:
            correct_answers += 1

    
    score_percentage = (correct_answers / total_questions) * 100

    
    final_result_message = f"Your final score is: {score_percentage:.2f}% based on {correct_answers}/{total_questions} correct answers."

    return final_result_message

   
