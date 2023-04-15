sciences = (
    {
        'name': 'Mathematics',
        'dependencies': [],
    },
    {
        'name': 'Philosophy',
        'dependencies': [],
    },
    {
        'name': 'Physics',
        'dependencies': ['Mathematics'],
    },
    {
        'name': 'Chemistry',
        'dependencies': ['Mathematics'],
    },
    {
        'name': 'Scientific method',
        'dependencies': ['Mathematics', 'Philosophy'],
    },
    {
        'name': 'Astrophysics',
        'dependencies': ['Chemistry', 'Physics'],
    },
    {
        'name': 'Electronics',
        'dependencies': ['Chemistry', 'Physics'],
    },
    {
        'name': 'Geology',
        'dependencies': ['Chemistry', 'Physics'],
    },
    {
        'name': 'Biology',
        'dependencies': ['Chemistry'],
    },
    {
        'name': 'Sociology',
        'dependencies': ['Philosophy', 'Biology'],
    },
    {
        'name': 'Economy',
        'dependencies': ['Mathematics', 'Philosophy'],
    },
    {
        'name': 'Energy',
        'dependencies': ['Chemistry', 'Physics', 'Economy'],
    },
    {
        'name': 'Construction',
        'dependencies': ['Physics', 'Sociology'],
    },
    {
        'name': 'Materials Science',
        'dependencies': ['Chemistry', 'Geology'],
    },
    {
        'name': 'Cybernetics',
        'dependencies': ['Mathematics', 'Philosophy', 'Electronics'],
    },
    {
        'name': 'Communications',
        'dependencies': ['Physics', 'Sociology', 'Cybernetics'],
    },
    {
        'name': 'Archeology',
        'dependencies': [
            'Scientific method',
            'Materials Science',
            'Sociology'
        ]
    },
    {
        'name': 'Nuclear physics',
        'dependencies': ['Chemistry', 'Physics'],
    },
    {
        'name': 'Thermonuclear fusion',
        'dependencies': ['Chemistry', 'Physics', 'Electronics'],
    },
    {
        'name': 'Robotics',
        'dependencies': ['Biology', 'Cybernetics'],
    },
    {
        'name': 'Espionage',
        'dependencies': ['Sociology', 'Communications', 'Cybernetics'],
    },
    {
        'name': 'Shipbuilding',
        'dependencies': [
            'Astrophysics',
            'Sociology',
            'Materials Science',
            'Robotics',
        ],
    },
    {
        'name': 'Warfare',
        'dependencies': ['Mathematics', 'Philosophy', 'Economy'],
    },
)
