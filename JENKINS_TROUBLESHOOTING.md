# Jenkins CI/CD Troubleshooting Guide

This guide provides solutions for common issues encountered with the Jenkins CI/CD pipeline for this chatbot project.

## Common Issues and Solutions

### 1. Jenkinsfile Syntax Errors

**Symptoms:**

- Build fails with error messages like "Expected a symbol", "Expected a stage", or "Undefined section"
- Pipeline doesn't start or stops at parsing stage

**Solution:**

- Ensure proper spacing between pipeline sections (agent, options, environment, etc.)
- Check for proper indentation in the Jenkinsfile
- Make sure all stages have proper curly braces and spacing
- Validate your Jenkinsfile with the Jenkins linter

**Example of correctly formatted stage:**

```groovy
stage('Test Stage') {
    steps {
        script {
            echo "Running tests"
        }
    }
}
```

### 2. Test Failures in CI Environment

**Symptoms:**

- Tests pass locally but fail in Jenkins
- Errors related to external services (AWS, Telegram)

**Solutions:**

- Use the minimal CI test suite for CI environments:
  ```bash
  python -m pytest tests/test_ci_minimal.py -v
  ```
- Skip integration tests in CI:
  ```bash
  pytest -m "not integration"
  ```
- Use proper environment variable checks:

  ```python
  import os
  import pytest

  @pytest.mark.skipif(os.environ.get('CI') == 'true',
                     reason="Test ignored in CI environment")
  def test_something():
      # Test code here
  ```

### 3. Shell Command Issues

**Symptoms:**

- Shell commands fail with different behavior in Jenkins vs local environment
- Path or command not found errors

**Solutions:**

- Use absolute paths when possible
- Explicitly specify the Python interpreter path:
  ```groovy
  sh "venv/bin/python -m pytest tests/test_ci_minimal.py"
  ```
- Use simpler command structures:
  ```groovy
  // Instead of complex conditionals:
  sh "venv/bin/python -m pytest tests/test_ci_minimal.py"
  ```

## Quick Fixes

If your build is failing in CI, try these quick fixes:

1. Run only the minimal tests:

   ```bash
   venv/bin/python -m pytest tests/test_ci_minimal.py -v
   ```

2. Skip the problematic test stages temporarily:

   ```groovy
   // In your Jenkinsfile
   stage('Tests') {
       when {
           expression { return false } // Temporarily skip this stage
       }
       steps {
           // ...
       }
   }
   ```

3. Manually check and format your Jenkinsfile:
   - Ensure proper spacing between sections
   - Check for missing curly braces
   - Verify all quotation marks are properly paired

## Contact

For help with this pipeline, please contact the DevOps team.
