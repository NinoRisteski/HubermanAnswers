import re

def print_vtt_metadata(file_path):
    """
    Prints the metadata of a VTT file, including number of cues and header information.
    
    Args:
    file_path (str): Path to the VTT file.
    """
    try:
        with open(/Users/fliprise/HubermanAnswers/data/docs, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Check for VTT file header
            if not content.startswith('WEBVTT'):
                print("Invalid VTT file.")
                return
            
            # Extract metadata/header information
            header = re.search(r'WEBVTT(.*?\n\n)', content, re.DOTALL)
            if header:
                print("Header Information:")
                print(header.group(1))
            else:
                print("No additional header info.")
            
            # Count the number of cues
            cues = re.findall(r'\n\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', content)
            print("Number of cues:", len(cues))
    
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
print_vtt_metadata('/Users/fliprise/HubermanAnswers/data/docs/ADHD & How Anyone Can Improve Their Focus ｜ Huberman Lab Podcast #37.mp3.vtt')
