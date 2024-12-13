# Use a heavy base image
FROM ubuntu:latest

# Set multiple environment variables in separate RUN commands
ENV APP_HOME=/app
RUN mkdir $APP_HOME
ENV PORT=8080
ENV DEBUG=true

# Install multiple packages with no cleanup
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN apt-get install -y wget
RUN apt-get install -y curl
RUN apt-get install -y git

# Copy entire context (potentially large)
COPY . /app

# Set working directory
WORKDIR /app

# Install dependencies with no optimization
RUN pip3 install Flask
RUN pip3 install requests
RUN pip3 install pandas
RUN pip3 install numpy
RUN pip3 install matplotlib
RUN pip3 install seaborn

# Add unnecessary files
RUN wget https://example.com/large-unnecessary-file.zip
RUN tar -xvf large-unnecessary-file.zip

# Expose port
EXPOSE 8080

# Simple command to run application
CMD ["python3", "app.py"]