# AI Classification API

A Django REST API that serves an Iris flower classification model. This project demonstrates how to deploy a machine learning model as a web service using Django and Docker.

## Features

- RESTful API built with Django REST Framework
- Machine Learning model (Logistic Regression) for Iris flower classification
- Docker containerization for easy deployment
- Model training script included
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

2. Build and start the Docker container:
```bash
docker-compose build
docker-compose up
```

The API will be available at `http://localhost:8000/api/predictor/`

## Local Development Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Train the model:
```bash
python train_model.py
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Prediction Endpoint
- URL: `/api/predictor/predict/`
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

## Project Structure

```
ai_classification_api/
├── core/                   # Django project settings
├── predictor/             # Main application
├── models_trained/        # Trained model files
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose configuration
├── requirements.txt       # Python dependencies
├── train_model.py         # Model training script
└── README.md             # This file
```

## Model Information

The classification model:
- Uses the Iris dataset
- Implements Logistic Regression
- Features: sepal length, sepal width, petal length, petal width
- Classes: setosa, versicolor, virginica
- Trained with 80/20 train/test split

## Development

To make changes to the project:

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and test them

3. Submit a pull request

## Testing

Run the tests with:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Iris dataset from scikit-learn
- Django REST Framework for API development
- scikit-learn for machine learning implementation
