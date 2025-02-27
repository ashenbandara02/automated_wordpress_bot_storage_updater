# Automated WordPress Bot Storage Updater

This repository provides a Python-based solution to automate the process of updating and managing storage in WordPress sites. By leveraging the WordPress REST API, this tool helps streamline content management tasks, reducing the need for manual intervention.

## Features

- **Automated Content Updates**: Schedule and execute content updates on your WordPress site without manual intervention.
- **Storage Management**: Efficiently manage and update storage configurations within your WordPress environment.
- **WordPress REST API Integration**: Seamlessly interact with your WordPress site using the WordPress REST API.

## Getting Started

### Prerequisites

Before using this tool, ensure you have the following:

- Python 3.7 or higher installed on your system.
- The `requests` Python library installed. If not, you can install it using:

  ```bash
  pip install requests
  ```

- A WordPress site with REST API access enabled.

### Configuration

1. **Generate an Application Password:**
   - Log in to your WordPress admin panel.
   - Go to **Users > Your Profile**.
   - Under **Application Passwords**, generate a new application password. This will be used for authentication when interacting with the WordPress REST API.

2. **Set Up the Script:**
   - Clone the repository:

     ```bash
     git clone https://github.com/ashenbandara02/automated_wordpress_bot_storage_updater.git
     ```

   - Navigate to the project directory:

     ```bash
     cd automated_wordpress_bot_storage_updater
     ```

### Usage

1. **Updating Content**: The main functionality of the bot is to update the content of WordPress posts. To update a post, edit the `update_content.py` script with the required WordPress site details and content to be updated.

2. **Run the Script**: You can run the script by executing the following command:

   ```bash
   python update_content.py
   ```

3. **Example Usage**:

   Here’s a sample script (`update_content.py`) to update a WordPress post:

   ```python
   import requests

   # WordPress site details
   wp_url = 'https://your-wordpress-site.com/wp-json/wp/v2/posts'
   wp_user = 'your_username'
   wp_app_password = 'your_application_password'

   # Content to update
   post_id = 123  # Replace with your post ID
   updated_content = {
       'title': 'Updated Post Title',
       'content': 'This is the updated content of the post.',
       'status': 'publish'  # Options: 'publish', 'draft', 'private'
   }

   # Authentication
   auth = (wp_user, wp_app_password)

   # Update the post
   response = requests.post(f'{wp_url}/{post_id}', json=updated_content, auth=auth)

   if response.status_code == 200:
       print('Post updated successfully.')
   else:
       print(f'Failed to update post: {response.status_code} - {response.text}')
   ```

   Ensure you replace `your-wordpress-site.com`, `your_username`, `your_application_password`, and the `post_id` with the correct details.

## Additional Resources

- [WordPress REST API Documentation](https://developer.wordpress.org/rest-api/)
- [Python Requests Library Documentation](https://docs.python-requests.org/en/latest/)

## Contributing

Feel free to fork the repository, open issues, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
