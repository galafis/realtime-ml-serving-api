# Documentation

This directory contains additional documentation and resources for the Real-Time ML Model Serving API.

## Architecture Diagrams

The `architecture_diagrams.py` script contains ASCII art diagrams that visualize the system architecture.

### Generating Diagrams

To view all architecture diagrams:

```bash
python3 docs/architecture_diagrams.py
```

### Available Diagrams

1. **System Architecture Diagram** - Shows the overall system structure with client applications, load balancer, ML server instances, Redis cache, and external services.

2. **Request Flow Diagram** - Illustrates the complete flow of a prediction request from client to response, including cache hit/miss scenarios.

3. **Data Flow Diagram** - Demonstrates how data flows through the system from training to serving phases.

4. **Deployment Architecture** - Shows the Kubernetes deployment setup with pods, services, ingress, and auto-scaling configuration.

### Using the Diagrams

These diagrams are also embedded in the main README.md file for easy reference. You can:

- Copy diagrams into presentations
- Include in documentation
- Use as reference for system understanding
- Share with team members

## Additional Documentation

For more detailed documentation, see:

- [README.md](../README.md) - Main project documentation
- [API.md](../API.md) - Complete API reference
- [ARCHITECTURE.md](../ARCHITECTURE.md) - Detailed system architecture
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide

## Contributing to Documentation

When contributing to documentation:

1. Keep diagrams simple and clear
2. Use ASCII art for portability
3. Update all language versions (English and Portuguese)
4. Include examples where appropriate
5. Ensure accuracy with current implementation

---

**Author:** Gabriel Demetrios Lafis  
**License:** MIT
