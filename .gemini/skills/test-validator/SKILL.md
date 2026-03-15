---
name: test-validator
description: Automatically check and update BDD test cases when new features are added to the project.
---

# Test Validator Skill

Use this skill to ensure that all new features are accompanied by relevant test cases and that existing tests are updated to reflect architectural changes.

## Workflow

1. **Review Changes**: Analyze the latest feature implementations in both frontend and backend.
2. **Scan Features**: Read existing `.feature` files in `tests/features/` to identify gaps.
3. **Identify Updates**:
    - Do existing scenarios need more detail (e.g., new mandatory fields)?
    - Are there new UI elements that require new locators?
    - Are there new API endpoints or response formats?
4. **Implement New Tests**: Add new scenarios to existing files or create new `.feature` files.
5. **Update Step Definitions**: Add or modify Python steps in `tests/features/steps/`.
6. **Verify**: Run the BDD suite to ensure 100% pass rate.

## Best Practices

- **API vs UI**: Always add tests for both the API layer and the UI layer for new features.
- **Negative Tests**: Don't forget to test unauthorized access or invalid data.
- **Data Isolation**: Use unique identifiers (like random suffixes) for test data to prevent collisions.
- **Locators**: Use resilient locators (like `get_by_label` or `get_by_role`) over fragile CSS selectors where possible.
