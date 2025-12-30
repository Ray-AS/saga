from backend.models.game import Choice, Intent

INTENT_MOD = {
    Intent.CAREFUL: 2,
    Intent.STANDARD: 0,
    Intent.BOLD: -2,
    Intent.DESPERATE: -4,
}


class CLIAdapter:
    def choose(self, choices: list[Choice]):
        for i, c in enumerate(choices, 1):
            print(f'{i}. {c.choice_description}')

        choice = input('> ')

        if choice == 'END':
            return 'END'

        return choices[int(choice) - 1]

    def choose_intent(self):
        for i, intent in enumerate(Intent, 1):
            print(f'{i}. {intent.value}')
        chosen = list(Intent)[int(input('> ')) - 1]
        return INTENT_MOD[chosen], chosen.value
