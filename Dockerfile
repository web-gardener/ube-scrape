FROM --platform=linux/amd64 ubuntu:latest

# Set the working directory to /application
WORKDIR /application

# Install Python and Miniconda
RUN apt-get update && apt-get install -y wget curl unzip chromium-browser libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1 && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3
    
ENV PATH=$PATH:/opt/miniconda3/bin

# Download and install Chrome browser
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

# Download and install ChromeDriver
RUN wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver

# Clean up
RUN rm chromedriver_linux64.zip

# Set the PATH environment variable
ENV PATH="/usr/local/bin:${PATH}"

# # Copy environment.yml and create conda environment
COPY environment.yml ./
RUN conda env create -f environment.yml

# # Copy code
COPY src ./

# # Run entrypoint
ENTRYPOINT ["/application/entrypoint.sh"]