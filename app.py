import requests
print(requests.__version__)

BASE_URL = "http://127.0.0.1:5000/api/"

def display_menu():
    print("\n" + "=" * 50)
    print("SIMPLE BLOG SYSTEM".center(50))
    print("=" * 50)
    print("1. View All Posts")
    print("2. View Post Details")
    print("3. Create New Post")
    print("4. Update Post")
    print("5. Delete Post")
    print("6. Exit")
    print("=" * 50)

def list_posts():
    try:
        response = requests.get(f"{BASE_URL}posts")
        if response.status_code == 200:
            posts = response.json()
            if not posts:
                print("\nNo posts found!")
                return

            print("\n" + "-" * 100)
            print(f"{'ID':<5}{'Title':<30}{'Author':<20}{'Tags':<20}{'Created At':<20}")
            print("-" * 100)
            for post in posts:
                print(f"{post['id']:<5}{post['title']:<30}{post['author']:<20}{post.get('tags', ''):<20}{post['created_at']:<20}")
            print("-" * 100)
        else:
            print(f"\nError fetching posts: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def view_post():
    post_id = input("\nEnter post ID: ")
    try:
        response = requests.get(f"{BASE_URL}posts/{post_id}")
        if response.status_code == 200:
            post = response.json()
            print("\n" + "-" * 50)
            print("POST DETAILS".center(50))
            print("-" * 50)
            print(f"ID: {post['id']}")
            print(f"Title: {post['title']}")
            print(f"Author: {post['author']}")
            print(f"Content:\n{post['content']}")
            print(f"Tags: {post.get('tags', 'N/A')}")
            print(f"Created At: {post['created_at']}")
            print(f"Updated At: {post.get('updated_at', 'Never')}")
            print("-" * 50)
        elif response.status_code == 404:
            print("\nPost not found!")
        else:
            print(f"\nError: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def add_post():
    print("\nEnter post details:")
    title = input("Title: ")
    content = input("Content: ")
    author = input("Author: ")
    tags = input("Tags (optional): ")

    if not title or not content or not author:
        print("\nTitle, content, and author are required!")
        return

    post_data = {
        "title": title,
        "content": content,
        "author": author,
        "tags": tags if tags else ''
    }

    try:
        response = requests.post(f"{BASE_URL}posts", json=post_data)
        if response.status_code == 201:
            print("\nPost added successfully!")
        else:
            print(f"\nError adding post: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def update_post():
    post_id = input("\nEnter post ID to update: ")

    try:
        response = requests.get(f"{BASE_URL}posts/{post_id}")
        if response.status_code != 200:
            print(f"\nError: {response.text if response.status_code != 404 else 'Post not found!'}")
            return

        current_post = response.json()
        print("\nCurrent post details:")
        print(f"1. Title: {current_post['title']}")
        print(f"2. Content: {current_post['content']}")
        print(f"3. Author: {current_post['author']}")
        print(f"4. Tags: {current_post.get('tags', 'N/A')}")

        print("\nEnter new values (leave blank to keep current):")
        updates = {}

        title = input("New title: ")
        if title: updates["title"] = title

        content = input("New content: ")
        if content: updates["content"] = content

        author = input("New author: ")
        if author: updates["author"] = author

        tags = input("New tags: ")
        if tags: updates["tags"] = tags

        if not updates:
            print("\nNo changes made!")
            return

        response = requests.put(f"{BASE_URL}posts/{post_id}", json=updates)
        if response.status_code == 200:
            print("\nPost updated successfully!")
        else:
            print(f"\nError updating post: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def delete_post():
    post_id = input("\nEnter post ID to delete: ")
    confirm = input(f"Are you sure you want to delete post {post_id}? (y/n): ")

    if confirm.lower() != 'y':
        print("Deletion cancelled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}posts/{post_id}")
        if response.status_code == 200:
            print("\nPost deleted successfully!")
        else:
            print(f"\nError deleting post: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def main():
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            list_posts()
        elif choice == '2':
            view_post()
        elif choice == '3':
            add_post()
        elif choice == '4':
            update_post()
        elif choice == '5':
            delete_post()
        elif choice == '6':
            print("\nExiting program Nakakadepress. Goodbye!!")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1-6.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main() 