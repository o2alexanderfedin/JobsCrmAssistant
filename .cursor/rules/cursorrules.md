# Cursor Development Rules

## General Development Process

1. **Understand First, Code Later**
   - Always analyze the existing code and logs thoroughly before making changes
   - Document your understanding of the issue before proposing solutions
   - Ask clarifying questions when needed

2. **Incremental Changes**
   - Make small, focused changes
   - Test each change before moving to the next
   - Document the impact of each change

3. **Testing Protocol**
   - Run affected tests after each change
   - Add new test cases for edge cases
   - Ensure all tests pass before committing

## Code Modification Rules

1. **Before Making Changes**
   - Review relevant code sections
   - Understand the current implementation
   - Identify potential side effects
   - Document the planned changes

2. **During Implementation**
   - Follow existing code style
   - Add appropriate logging
   - Update documentation
   - Keep changes minimal and focused

3. **After Changes**
   - Run tests
   - Review logs
   - Fix any linter errors
   - Document any remaining issues

## Debugging Process

1. **Initial Investigation**
   - Review error messages and logs
   - Identify the specific failure point
   - Document the current behavior

2. **Debug Strategy**
   - Add detailed logging
   - Test assumptions
   - Isolate the problem
   - Create minimal reproduction case

3. **Solution Implementation**
   - Propose solution with explanation
   - Implement changes incrementally
   - Verify fix with tests
   - Document the resolution

## Documentation Requirements

1. **Code Changes**
   - Update docstrings
   - Add inline comments for complex logic
   - Update README if needed

2. **Logging**
   - Add appropriate log levels
   - Include relevant context
   - Use consistent format

3. **Commit Messages**
   - Clear and descriptive
   - Reference related issues
   - Document breaking changes

## Quality Standards

1. **Code Quality**
   - Follow PEP 8 guidelines
   - Fix linter warnings
   - Maintain consistent style

2. **Testing**
   - Maintain test coverage
   - Add tests for new features
   - Update existing tests as needed

3. **Performance**
   - Consider efficiency
   - Avoid unnecessary operations
   - Profile when needed

## Communication Guidelines

1. **Status Updates**
   - Regular progress reports
   - Clear blockers identification
   - Document decisions made

2. **Code Reviews**
   - Detailed explanations
   - Reference relevant documentation
   - Address all feedback

3. **Issue Tracking**
   - Update issue status
   - Link related changes
   - Document workarounds 