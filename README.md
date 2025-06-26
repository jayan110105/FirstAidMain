# First Aid Training - Interactive Web Application

A Django-based interactive web application for first aid training with learning modules, quizzes, and real-life scenarios.

## Features

- **Interactive Learning Modules:** Engaging modules covering a wide range of first aid topics:
  - Burns
  - Choking
  - Cardiac Emergencies
  - Fractures and Sprains
  - Allergic Reactions
  - Cold and Heat-Related Emergencies
  - Poisoning
  - Venomous Bites and Stings
  - Wound Care

- **Quizzes:** Test your knowledge with quizzes at the end of each learning module.

- **Real-life Scenarios:** Apply your skills in interactive scenarios, including:
  - Hiking Trip Emergencies
  - Restaurant Incidents
  - Burn Emergencies

- **User Profiles & Progression:**
  - User registration and login
  - Personal user profiles
  - Track your progress and view achievements
  - See how you rank on the leaderboard

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Python](https://www.python.org/downloads/) (version 3.8 or higher recommended)
- [Pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/jayan110105/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create and activate a virtual environment:**
    - On Windows:
      ```sh
      python -m venv venv
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      python3 -m venv venv
      source venv/bin/activate
      ```

3.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```sh
    python manage.py migrate
    ```

5.  **Create a superuser to access the admin panel:**
    ```sh
    python manage.py createsuperuser
    ```
    Follow the prompts to create a username and password.

### Running the Application

1.  **Start the development server:**
    ```sh
    python manage.py runserver
    ```

2.  Open your web browser and navigate to `http://127.0.0.1:8000/` to see the application.
    - You can access the admin panel at `http://127.0.0.1:8000/admin/`.
