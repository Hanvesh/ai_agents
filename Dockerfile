FROM 482341158969.dkr.ecr.ap-south-1.amazonaws.com/ubuntu22-04-arm:ubuntu22

# Install necessary packages using apt
RUN apt-get update && \
    apt-get install -y iputils-ping findutils curl telnet dnsutils  && \
    groupadd -r mpokket && \
    adduser --system --uid 1001 --ingroup mpokket resume-builder-rag

RUN pip3 

RUN python3 

#RUN cp -r /root/nltk_data /usr/local/share/nltk_data

# Set working directory
WORKDIR /usr/src/app

COPY ./requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .


RUN chown -R resume-builder-rag:mpokket /usr/src/app
USER resume-builder-rag
# Switch to the new user

RUN whoami

# Expose port
EXPOSE 8102

# Set entrypoint
ENTRYPOINT ["/bin/bash", "./startup.sh"]
