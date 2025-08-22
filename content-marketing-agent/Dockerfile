# Use Apify's Node.js base image with Python support
FROM apify/actor-node-python:20

# Copy all files to the container
COPY . ./

# Install Node.js dependencies
RUN npm install --quiet --only=prod --no-optional

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the command to run the actor
CMD ["npm", "start"]