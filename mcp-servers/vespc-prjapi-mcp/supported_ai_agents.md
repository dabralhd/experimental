# Supported AI Agents in STAIoT Craft

This document outlines the AI agents and model types supported by the STAIoT Craft Project API.

## Model Types (AI Agents)

The STAIoT Craft platform supports the following AI agent types:

### 1. Classifier
- **Type**: `classifier`
- **Description**: Classification models for categorizing data into predefined classes
- **Use Cases**: 
  - Image classification
  - Text classification
  - Sensor data classification
  - Pattern recognition
- **Features**:
  - Supports multiple classes
  - Can be trained on various datasets
  - Suitable for IoT sensor data analysis

### 2. Anomaly Detector
- **Type**: `anomaly_detector`
- **Description**: Models designed to detect unusual patterns or outliers in data
- **Use Cases**:
  - Fault detection in industrial equipment
  - Network security monitoring
  - Quality control in manufacturing
  - Predictive maintenance
- **Features**:
  - Real-time anomaly detection
  - Threshold-based alerting
  - Suitable for time-series data

## Training Types

The platform supports two training approaches:

### 1. Offline Training
- **Type**: `offline`
- **Description**: Traditional batch training on historical data
- **Use Cases**:
  - Initial model development
  - Large dataset training
  - Model fine-tuning

### 2. Online Training
- **Type**: `online`
- **Description**: Continuous learning from streaming data
- **Use Cases**:
  - Real-time model adaptation
  - Incremental learning
  - Adaptive systems

## Tool Support

The platform includes various tools for model development and deployment:

### Tool Properties
- **name**: Tool identifier
- **description**: Tool description
- **version**: Tool version
- **container_name**: Container name (optional)
- **container_version**: Container version (optional)
- **parameters**: Tool-specific parameters

## Project Structure

Each AI project can contain:
- Multiple models of different types
- Various training activities
- Deployment configurations
- Artifacts and reports

## API Endpoints

The following endpoints support AI agent operations:

- `/templates/projects` - Get template projects
- `/projects` - Manage user projects
- `/projects/{project_name}/models` - Manage models
- `/projects/{project_name}/models/{model_name}/{activity_type}` - Manage training activities
- `/projects/{project_name}/deployments` - Manage deployments

## Example Usage

```python
# Create a classifier model
new_model = NewModel(
    name="my_classifier",
    model_type=ModelType.CLASSIFIER,
    training_type=TrainingType.OFFLINE,
    classes=["class1", "class2", "class3"]
)

# Create an anomaly detector
new_model = NewModel(
    name="my_anomaly_detector", 
    model_type=ModelType.ANOMALY_DETECTOR,
    training_type=TrainingType.ONLINE
)
```

## Supported Platforms

The AI agents can be deployed on:
- Edge devices (leaf nodes)
- Gateway devices
- Cloud platforms
- Hybrid deployments

## Integration Capabilities

- REST API access
- MCP (Model Context Protocol) server support
- Real-time data processing
- Cloud-native deployment
- IoT device integration 