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

## Repository Management

1. **GitHub CLI Usage**
   - Use GitHub CLI (`gh`) for repository operations whenever possible
   - Create repositories using `gh repo create`
   - Manage issues and PRs through CLI
   - Use CLI for repository settings and configuration
   - Prefer CLI over manual GitHub web interface operations

2. **Version Control**
   - Keep commits atomic and focused
   - Write clear commit messages
   - Use feature branches for new development
   - Maintain clean git history

3. **Branch Structure**
   - `main` - Production-ready code, always stable
   - `develop` - Integration branch for features, main development branch
   - `feature/*` - New features and enhancements (e.g., `feature/job-search`)
   - `bugfix/*` - Bug fixes (e.g., `bugfix/resume-parser`)
   - `hotfix/*` - Urgent production fixes
   - `release/*` - Release preparation branches
   - Branch naming: `type/issue-number-short-description`
   - Delete branches after merging
   - Keep branches up to date with develop

4. **Branch Workflow Rules**
   - **Feature Development**:
     - Create feature branch from `develop`: `git checkout -b feature/123-feature-name develop`
     - Develop and test feature
     - Keep feature branch updated with develop: `git rebase develop`
     - For solo development: Direct push to `develop` is allowed
     - For team development: Create PR to merge into `develop`
     - Delete feature branch after merging

   - **Bug Fixes**:
     - Create bugfix branch from `develop`: `git checkout -b bugfix/456-bug-description develop`
     - Fix and test the bug
     - For solo development: Direct push to `develop` is allowed
     - For team development: Create PR to merge into `develop`
     - Delete bugfix branch after merging

   - **Hotfixes**:
     - Create hotfix branch from `main`: `git checkout -b hotfix/789-hotfix-description main`
     - Fix and test the issue
     - For solo development: Direct push to both `main` and `develop` is allowed
     - For team development: Create PR to merge into both `main` and `develop`
     - Delete hotfix branch after merging

   - **Releases**:
     - Version format: `vX.Y.Z` (e.g., v1.0.0)
       - X: Major version (breaking changes)
       - Y: Minor version (new features)
       - Z: Patch version (bug fixes)
     - Release branch creation:
       ```bash
       # From develop branch
       git checkout develop
       git pull origin develop
       
       # Create release branch
       git checkout -b release/v1.0.0
       
       # Update version numbers and changelog
       # Commit changes with message: "chore(release): prepare v1.0.0"
       
       # Push release branch
       git push -u origin release/v1.0.0
       ```
     - Release process:
       1. Create release branch from `develop`
       2. Update version numbers in code
       3. Update CHANGELOG.md
       4. Commit changes with release preparation message
       5. For solo development: 
          - Merge to `main`: `git checkout main && git merge release/v1.0.0`
          - Tag release: `git tag -a v1.0.0 -m "Release v1.0.0"`
          - Push changes: `git push origin main --tags`
          - Merge to `develop`: `git checkout develop && git merge main`
       6. For team development:
          - Create PRs to merge into both `main` and `develop`
          - After approval, merge to both branches
          - Tag the release in `main`
       7. Delete release branch after merging

5. **Commit Message Rules**
   - Format: `type(scope): description`
   - Types:
     - `feat`: New feature
     - `fix`: Bug fix
     - `docs`: Documentation changes
     - `style`: Code style changes (formatting, etc.)
     - `refactor`: Code refactoring
     - `test`: Adding or modifying tests
     - `chore`: Maintenance tasks
   - Scope: Component or module affected
   - Description: Clear, concise explanation
   - Example: `feat(job-search): add LinkedIn job board integration`

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