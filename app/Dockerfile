# Extend the official Rasa SDK image
FROM rasa/rasa-sdk

# Copy any additional custom requirements, if necessary (uncomment next line)
COPY ./requirements.txt /app

# Change to user
USER root

# Install extra requirements for actions code, if necessary (uncomment next line)
RUN pip install -r /app/requirements.txt
RUN python -m spacy download en_core_web_md

# Copy actions folder to working directory
COPY ./actions /app/actions