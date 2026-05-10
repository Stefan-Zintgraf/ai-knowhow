# Claude Code Training Exercises

This directory contains hands-on exercises for the Claude Code training course. Each exercise is designed to demonstrate specific Claude Code capabilities across different programming languages and frameworks.

## Structure

The exercises are organized by programming language:

```
exercises/
├── python/
│   ├── weather-app/        # API integration and testing exercise
│   └── flask-api/          # Legacy code refactoring exercise
├── javascript/
│   ├── lyrics-trainer/     # Frontend refactoring and documentation
│   └── api-client/         # Test generation and error handling
└── java/
    ├── spring-boot-service/  # Modern Java refactoring
    ├── certificate-service/  # Spring Boot PDF generation
    └── shopping-service/     # REST API development
```

## Getting Started

Each exercise directory contains:
- `README.md` - Exercise instructions and objectives
- Source code to work with
- `EXERCISE.md` - Specific tasks to complete with Claude Code

## Exercise Types

### 1. Code Exploration & Understanding
- Navigate unfamiliar codebases
- Identify architecture patterns
- Trace execution flows

### 2. Refactoring & Modernization
- Update legacy code to modern patterns
- Improve code quality and readability
- Apply language-specific best practices

### 3. Test Generation
- Create comprehensive test suites
- Identify edge cases
- Implement test-driven development

### 4. Documentation Creation
- Generate README files
- Add inline code comments
- Create API documentation

### 5. Debugging & Bug Fixing
- Analyze error messages
- Trace issues to root causes
- Implement fixes with tests

## Prerequisites

- Claude Code installed and configured
- Development environments for Python, JavaScript/Node.js, and Java
- Basic familiarity with the respective languages

## Using These Exercises

1. Navigate to an exercise directory
2. Read the exercise README.md
3. Start Claude Code: `claude`
4. Follow the exercise instructions
5. Use different Claude Code modes (default, auto-accept, plan mode) as appropriate

## Tips for Success

- Start with simpler exercises if you're new to Claude Code
- Use Plan Mode (`Shift+Tab+Tab`) for complex refactoring
- Create git branches before major changes
- Commit frequently to create checkpoints
- Review Claude's suggestions before accepting

## Language-Specific Setup

### Python
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### JavaScript/Node.js
```bash
# Install dependencies
npm install
# or
pnpm install
```

### Java/Spring Boot
```bash
# Using Maven
mvn clean install

# Using Gradle
./gradlew build
```

## Exercise Progression

1. **Beginner**: Start with weather-app (Python) or api-client (JavaScript)
2. **Intermediate**: Try spring-boot-service or flask-api refactoring
3. **Advanced**: Tackle certificate-service or shopping-service full implementation

## Need Help?

- Refer to the main course slides
- Check the exercise-specific README files
- Use Claude Code to explain unfamiliar code
- Ask your instructor during the training session