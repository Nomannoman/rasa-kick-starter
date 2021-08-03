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
#RUN cp /app/actions/xpdf-tools-linux-4.03/bin64/pdftotext /usr/local/bin
RUN apt-get update
RUN apt-get install poppler-utils -y

COPY ./actions /app/actions

#RUN apt-get install libfontconfig1 fontconfig libfontconfig1-dev libfontconfig -y
#RUN pip install pdftotext
#RUN apt-get update
