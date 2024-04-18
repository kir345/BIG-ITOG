def make_sequence_steps_article(sequence_steps: str):
    steps = sequence_steps.split('\n')
    return steps


if __name__ == '__main__':
    with open('../dev-local/sequence_steps_example', 'r') as f:
        text = f.readlines()
    text = ''.join(text)
    text = make_sequence_steps_article(text)
    print(text)