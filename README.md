# AI Classification API

A Django REST API that serves an Iris flower classification model. This project demonstrates how to deploy a machine learning model as a web service using Django and Docker.

## Features

- RESTful API built with Django REST Framework
- Machine Learning model (Logistic Regression) for Iris flower classification
- Docker containerization for easy deployment
- Automated model training and testing
- Comprehensive test suite
- Scalable architecture

## Prerequisites

- Docker and Docker Compose
- Python 3.12 (if running locally)
- Git

## Quick Start with Docker

1. Clone the repository:
```bash
git clone <your-repository-url>
cd ai_classification_api
```

2. Build and start the services:
```bash
# Build the Docker images
docker-compose build

# Train the model and run tests
docker-compose run test

# Start the API service
docker-compose up web
```

The API will be available at `http://localhost:8000/api/predict/`

## Project Structure

```
ai_classification_api/
├── core/                   # Django project settings
├── predictor/             # Main application
│   ├── models_trained/    # Directory for trained ML models
│   ├── management/        # Django management commands
│   ├── tests.py          # Test suite
│   ├── views.py          # API views
│   ├── urls.py           # URL routing
│   └── serializers.py    # Data serializers
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── train_model.py         # Model training script
└── README.md             # This file
```

## Development Workflow

### Running Tests
Tests can be run in the Docker environment:
```bash
# Run all tests with model training
docker-compose run test

# Run specific test modules
docker-compose run test python manage.py test predictor.tests.ModelTests
docker-compose run test python manage.py test predictor.tests.APITests
```

### Training the Model
The model is automatically trained when running tests, but you can also train it separately:
```bash
docker-compose run web python train_model.py
```

### API Usage

#### Prediction Endpoint
- URL: `/api/predict/`
- Method: `POST`
- Input Format:
```json
{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}
```
- Output Format:
```json
{
    "prediction": "setosa",
    "probability": 0.95
}
```

## Model Information

The classification model:
- Uses the Iris dataset from scikit-learn
- Implements Logistic Regression
- Features: sepal length, sepal width, petal length, petal width
- Classes: setosa, versicolor, virginica
- Trained with 80/20 train/test split
- Achieves ~96% accuracy on test set

## Docker Commands

Common Docker operations:
```bash
# Build containers
docker-compose build

# Start services
docker-compose up web

# Run with detached mode
docker-compose up -d web

# Stop services
docker-compose down

# View logs
docker-compose logs web

# Run tests
docker-compose run test

# Remove all containers and volumes
docker-compose down -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Testing

The project includes comprehensive tests covering:
- Model functionality
- API endpoints
- Data validation
- Edge cases

Run the full test suite with:
```bash
docker-compose run test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Iris dataset from scikit-learn
- Django REST Framework for API development
- scikit-learn for machine learning implementation
