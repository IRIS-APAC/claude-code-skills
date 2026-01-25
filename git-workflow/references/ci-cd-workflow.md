# CI/CD Workflow

Continuous Integration and Continuous Deployment automation for professional software development.

## Overview

**CI/CD** automates the process of building, testing, and deploying code changes to ensure fast, reliable releases.

**Continuous Integration (CI)**:
- Automatically build and test code on every commit/PR
- Catch bugs and integration issues early
- Ensure code quality standards are met

**Continuous Deployment (CD)**:
- Automatically deploy passing code to environments
- Enable fast, frequent releases
- Reduce manual deployment errors

---

## ⚠️ CRITICAL: Secure Authentication for GitHub Actions

**NEVER use long-lived credentials in GitHub Actions workflows!**

**❌ INSECURE (Don't do this)**:
```yaml
# BAD: Storing AWS Access Keys or Azure Client Secrets as GitHub Secrets
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  AZURE_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
```

**Problems with this approach**:
- Developers with write access can exfiltrate secrets via workflows
- Secrets never expire (permanent access if stolen)
- Must rotate manually (easy to forget)
- Broad attack surface (stored in GitHub)

**✅ SECURE (Use zero-secrets architecture)**:
```yaml
# GOOD: Use OIDC for temporary credentials (no secrets stored)
permissions:
  id-token: write  # Required for OIDC
  contents: read

- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/github-deploy
    aws-region: ap-southeast-2
    # NO AWS_ACCESS_KEY_ID or AWS_SECRET_ACCESS_KEY needed!
```

**Benefits of OIDC**:
- ✅ No secrets to steal (workflow only has public role ARN)
- ✅ Credentials auto-expire (1 hour validity)
- ✅ Granular access control (specific repo/branch)
- ✅ Complete audit trail (CloudTrail shows which workflow accessed what)

**📖 For complete authentication patterns, see**:
- `developer-analysis/references/authentication-patterns.md` - Zero-secrets architecture guide
- Covers GitHub Actions → AWS/Azure, AWS → Azure, local development, JWT validation

**The examples below show long-lived credentials for educational purposes. In production, ALWAYS use OIDC instead.**

---

## CI Pipeline (Automated Testing and Building)

**What runs on every PR/commit**:
1. **Linting and Formatting** - Enforce code style
2. **Unit Tests** - Fast, isolated tests
3. **Integration Tests** - Component interaction tests
4. **Build** - Compile/bundle application
5. **Security Scanning** - Check for vulnerabilities
6. **Coverage Check** - Enforce minimum coverage (80%)

### GitHub Actions Example

**File**: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install ruff black mypy
          pip install -r requirements.txt

      - name: Run ruff (linter)
        run: ruff check src/

      - name: Run black (formatter)
        run: black --check src/

      - name: Run mypy (type checker)
        run: mypy src/

  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pytest pytest-cov
          pip install -r requirements.txt

      - name: Run tests with coverage
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
        run: |
          pytest --cov=src --cov-report=term --cov-report=xml tests/

      - name: Check coverage threshold
        run: |
          coverage report --fail-under=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: true

  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Build package
        run: |
          pip install build
          python -m build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Bandit (security linter)
        run: |
          pip install bandit
          bandit -r src/

      - name: Run safety (dependency vulnerability scanner)
        run: |
          pip install safety
          safety check --json

      - name: Run Trivy (container vulnerability scanner)
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
```

### GitLab CI Example

**File**: `.gitlab-ci.yml`

```yaml
stages:
  - lint
  - test
  - build
  - security

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  POSTGRES_DB: testdb
  POSTGRES_USER: postgres
  POSTGRES_PASSWORD: postgres

cache:
  paths:
    - .cache/pip

lint:
  stage: lint
  image: python:3.11
  script:
    - pip install ruff black mypy
    - pip install -r requirements.txt
    - ruff check src/
    - black --check src/
    - mypy src/

test:
  stage: test
  image: python:3.11
  services:
    - postgres:15
    - redis:7
  variables:
    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/testdb
    REDIS_URL: redis://redis:6379
  script:
    - pip install pytest pytest-cov
    - pip install -r requirements.txt
    - pytest --cov=src --cov-report=term --cov-report=xml tests/
    - coverage report --fail-under=80
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

build:
  stage: build
  image: python:3.11
  script:
    - pip install build
    - python -m build
  artifacts:
    paths:
      - dist/

security:
  stage: security
  image: python:3.11
  script:
    - pip install bandit safety
    - bandit -r src/
    - safety check
```

## CD Pipeline (Automated Deployment)

**What runs on successful merge to develop/main**:
1. **Build Production Artifacts** - Optimised build for deployment
2. **Deploy to Environment** - Staging (develop) or Production (main)
3. **Run Smoke Tests** - Verify critical functionality
4. **Health Checks** - Ensure deployment is healthy
5. **Rollback on Failure** - Automatic rollback if deployment fails

### Environment Strategy

| Branch | Environment | Purpose | Auto-Deploy |
|--------|-------------|---------|-------------|
| `develop` | Staging | Integration testing, QA | ✅ Yes |
| `main` | Production | Live users | ✅ Yes (or manual approval) |
| `feature/*` | Preview/Dev | Feature testing | ⚠️ Optional |

### GitHub Actions Deployment Example

**File**: `.github/workflows/deploy-staging.yml`

```yaml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Build application
        run: |
          python -m build

      - name: Deploy to staging
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          # Example: Deploy to AWS Elastic Beanstalk
          pip install awsebcli
          eb deploy staging-env

      - name: Run smoke tests
        run: |
          pytest tests/smoke/ --base-url=https://staging.example.com

      - name: Notify team
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Staging deployment ${{ job.status }}: ${{ github.sha }}"
            }
```

**File**: `.github/workflows/deploy-production.yml`

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Build application
        run: |
          python -m build

      - name: Deploy to production
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          pip install awsebcli
          eb deploy production-env

      - name: Run smoke tests
        run: |
          pytest tests/smoke/ --base-url=https://example.com

      - name: Create deployment tag
        run: |
          git tag -a "v$(date +'%Y%m%d-%H%M%S')" -m "Production deployment"
          git push origin --tags

      - name: Notify team
        if: always()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "Production deployment ${{ job.status }}: ${{ github.sha }}"
            }
```

## Deployment Strategies

### 1. Blue-Green Deployment

**How it works**:
- Run two identical environments (blue and green)
- Blue is live, deploy to green
- Switch traffic from blue to green
- Keep blue as instant rollback option

**Benefits**:
- ✅ Zero-downtime deployments
- ✅ Instant rollback
- ✅ Full testing in production environment before switching

**Use when**:
- High availability required
- Instant rollback critical
- Can afford duplicate infrastructure

### 2. Canary Deployment

**How it works**:
- Deploy to small subset of servers (5-10%)
- Monitor metrics (errors, latency, user feedback)
- Gradually increase traffic to new version
- Rollback if issues detected

**Benefits**:
- ✅ Low-risk deployments
- ✅ Real-world validation with minimal user impact
- ✅ Gradual rollout

**Use when**:
- Want to validate changes with real traffic
- Risk-averse deployments
- Microservices architecture

### 3. Rolling Deployment

**How it works**:
- Update servers one at a time or in batches
- Always maintain some servers on old version
- Gradually roll out to all servers

**Benefits**:
- ✅ No additional infrastructure required
- ✅ Gradual rollout
- ✅ Can pause/resume deployment

**Use when**:
- Infrastructure cost is a concern
- Can tolerate brief inconsistency between versions
- Standard web applications

## Environment Management

### Environment Variables

**Store secrets securely** (never commit to repository):

**GitHub Actions Secrets**:
1. Go to repository → Settings → Secrets and variables → Actions
2. Add secrets:
   - `DATABASE_URL`
   - `API_KEY`
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

**GitLab CI/CD Variables**:
1. Go to repository → Settings → CI/CD → Variables
2. Add protected and masked variables for sensitive data

**Environment-specific configuration**:

```yaml
# .github/workflows/deploy.yml
jobs:
  deploy-staging:
    environment:
      name: staging
    env:
      APP_ENV: staging
      DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
      API_URL: https://staging-api.example.com

  deploy-production:
    environment:
      name: production
    env:
      APP_ENV: production
      DATABASE_URL: ${{ secrets.PROD_DATABASE_URL }}
      API_URL: https://api.example.com
```

### Infrastructure as Code (IaC)

**Store infrastructure configuration in repository**:

**Terraform example**:
```hcl
# terraform/main.tf
resource "aws_elastic_beanstalk_environment" "staging" {
  name                = "my-app-staging"
  application         = aws_elastic_beanstalk_application.app.name
  solution_stack_name = "64bit Amazon Linux 2023 v4.0.0 running Python 3.11"

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = "t3.small"
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MinSize"
    value     = "2"
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MaxSize"
    value     = "4"
  }
}
```

## Database Migrations in CI/CD

**CRITICAL**: Run database migrations as part of deployment pipeline.

### Migration Strategy

**Backwards-compatible migrations** (safest):
1. Deploy code that works with both old and new schema
2. Run migration
3. Deploy code that requires new schema

**Example GitHub Actions migration step**:

```yaml
- name: Run database migrations
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
  run: |
    # Check current migration status
    python manage.py showmigrations

    # Run migrations
    python manage.py migrate

    # Verify migrations applied
    python manage.py showmigrations --list
```

**Migration rollback plan**:
- ✅ Always create down migrations
- ✅ Test rollback in staging first
- ✅ Have rollback script ready for production

## Rollback Procedures

### Automatic Rollback (GitHub Actions)

```yaml
- name: Deploy to production
  id: deploy
  run: |
    eb deploy production-env

- name: Run health checks
  id: health_check
  run: |
    ./scripts/health-check.sh https://example.com

- name: Rollback on failure
  if: failure()
  run: |
    # Revert to previous version
    eb deploy production-env --version previous

    # Or: Switch back to blue environment (blue-green)
    # aws elbv2 modify-rule --rule-arn $RULE_ARN --actions TargetGroupArn=$BLUE_TG

- name: Notify on rollback
  if: failure()
  run: |
    echo "Deployment failed, rolled back to previous version"
```

### Manual Rollback

**For emergency rollbacks**:

```bash
# Revert to specific git commit
git revert <commit-hash>
git push origin main

# Or: Deploy previous Docker image
kubectl set image deployment/my-app my-app=my-app:previous-tag

# Or: Switch traffic back to blue environment
aws elbv2 modify-rule --rule-arn $RULE_ARN --actions TargetGroupArn=$BLUE_TG
```

## Monitoring and Alerts

**Post-deployment monitoring**:

```yaml
- name: Monitor deployment
  run: |
    # Check error rate
    ERROR_RATE=$(curl -s https://api.example.com/metrics | jq '.error_rate')
    if (( $(echo "$ERROR_RATE > 0.05" | bc -l) )); then
      echo "Error rate too high: $ERROR_RATE"
      exit 1
    fi

    # Check response time
    RESPONSE_TIME=$(curl -s https://api.example.com/metrics | jq '.avg_response_time')
    if (( $(echo "$RESPONSE_TIME > 500" | bc -l) )); then
      echo "Response time too high: $RESPONSE_TIME ms"
      exit 1
    fi
```

**Alert on failures**:

```yaml
- name: Send alert on failure
  if: failure()
  uses: actions/github-script@v7
  with:
    script: |
      github.rest.issues.create({
        owner: context.repo.owner,
        repo: context.repo.repo,
        title: 'Deployment Failed: ' + context.sha,
        body: 'CI/CD pipeline failed. Check logs: ' + context.serverUrl + '/' + context.repo.owner + '/' + context.repo.repo + '/actions/runs/' + context.runId,
        labels: ['deployment', 'urgent']
      })
```

## Best Practices

### CI/CD Configuration

✅ **DO**:
- Run CI on every PR and commit
- Enforce coverage thresholds (80% minimum)
- Run security scans automatically
- Deploy to staging automatically on develop merge
- Require manual approval for production deployments (initially)
- Tag production deployments with version numbers
- Run smoke tests after deployment
- Monitor deployments for errors
- Have automatic rollback on health check failures

❌ **DON'T**:
- Commit secrets to repository (use CI/CD secrets)
- Deploy without running tests
- Deploy breaking migrations without backwards compatibility
- Skip staging deployments
- Deploy on Friday afternoon (if possible)
- Ignore test failures to "ship faster"

### Deployment Checklist

**Before deploying to production**:
- [ ] All tests pass in CI
- [ ] Code reviewed and approved
- [ ] Deployed and tested in staging
- [ ] Database migrations tested in staging
- [ ] Rollback plan documented
- [ ] Team notified of deployment
- [ ] Monitoring dashboards open
- [ ] On-call engineer available

## Platform-Specific Examples

### Deploy to AWS Elastic Beanstalk

```yaml
- name: Deploy to AWS Elastic Beanstalk
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  run: |
    pip install awsebcli
    eb init -p python-3.11 my-app --region us-east-1
    eb deploy production-env
```

### Deploy to Google Cloud Run

```yaml
- name: Deploy to Google Cloud Run
  uses: google-github-actions/deploy-cloudrun@v2
  with:
    service: my-app
    region: us-central1
    image: gcr.io/my-project/my-app:${{ github.sha }}
    env_vars: |
      DATABASE_URL=${{ secrets.DATABASE_URL }}
      API_KEY=${{ secrets.API_KEY }}
```

### Deploy to Heroku

```yaml
- name: Deploy to Heroku
  env:
    HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
  run: |
    git remote add heroku https://git.heroku.com/my-app.git
    git push heroku main
```

### Deploy to Kubernetes

```yaml
- name: Deploy to Kubernetes
  run: |
    kubectl set image deployment/my-app my-app=my-app:${{ github.sha }}
    kubectl rollout status deployment/my-app
```

## Australian English

All CI/CD configuration, documentation, and messages use **Australian English spelling**:
- ✅ optimise, organisation, authorisation
- ❌ optimize, organization, authorization

## Related Documentation

- **git-workflow/SKILL.md** - Git branching and PR workflow
- **testing/SKILL.md** - Test strategy and coverage targets
- **developer-analysis/SKILL.md** - Documentation standards, ADRs

## Further Reading

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
- [12-Factor App: Build, release, run](https://12factor.net/build-release-run)
- [Continuous Delivery](https://continuousdelivery.com/) by Jez Humble
