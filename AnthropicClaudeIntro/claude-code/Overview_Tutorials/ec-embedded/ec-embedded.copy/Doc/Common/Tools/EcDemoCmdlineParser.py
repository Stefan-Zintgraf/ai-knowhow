import re
import json
import logging
import argparse

# Set up logging to include both debug and info levels
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_distance_to_second_word(text):
    """
    Calculate the distance to the second word in the given text.
    Returns the index of the second word if it exists, otherwise returns None.
    """
    logging.debug(f"Calculating distance to the second word in text: {text}")
    words = text.split()
    return text.find(words[1]) if len(words) > 1 else None

def remove_else_endif_blocks(matches):
    """
    Remove text between #else and #endif directives.
    """
    logging.debug("Removing text between #else and #endif")
    return re.sub(r'#else\s*(.*?)#endif', '', matches, flags=re.DOTALL)

def extract_log_messages_from_function(cpp_code):
    """
    Extract and process log messages from function definitions in the given C++ code.
    """
    logging.debug("Extracting log messages from function")
    function_pattern = re.compile(
        r'EC_T_VOID (ShowSyntaxApp|ShowSyntaxCommon|ShowSyntaxLinkLayer)\s*\(.*?\)\s*{(.*?)}',
        re.DOTALL
    )
    matches = function_pattern.findall(cpp_code)
    filtered_matches = [(m[0], remove_else_endif_blocks(m[1])) for m in matches]

    options = []
    seen_options = set()  # To avoid duplicating options
    
    def process_option(option):
        """
        Append the current option to the options list and track it as seen.
        """
        if option:
            logging.debug(f"Appending option: {option}")
            options.append(option)
            seen_options.add(option["name"])
        return None

    for func_name, func_body in filtered_matches:
        # Regex patterns for extracting log messages and options
        log_messages = re.findall(r'EcLogMsg\([^,]+,\s*\([^,]+,\s*[^,]+,\s*"([^"]*)"(?:,\s*[^)]+)?\)\);', func_body, re.MULTILINE)
        current_option, refboard_detected, refboard_bracflag, refboard_unbracflag, custom_args, distance = None, False, False, False, [], 2
        
        for message in log_messages:
            if "[RefBoard:" in message:
                refboard_description = message.split("[RefBoard:", 1)[1].strip()
                refboard_detected, refboard_bracflag = True, True
                logging.debug(f"Detected [RefBoard with description: {refboard_description}")
                if "]" in message:
                    refboard_detected, refboard_bracflag = False, False
                    if current_option:
                        current_option["args"][-1]["custom"] = custom_args
                    custom_args = []
                if current_option:
                    current_option["args"].append({
                        "arg": "RefBoard",
                        "arg_description": "[RefBoard: " + refboard_description,
                        "optional": "Yes",
                        "custom": custom_args
                    })
                custom_args = []
                
            elif refboard_bracflag:
                # Handle custom arguments within a RefBoard block
                if "if custom" in message:
                    custom_match = re.search(r'if custom\s+([\w\[\]:]+)\s*:\s*(.*)', message)
                    if custom_match:
                        custom_args.append({
                            "arg": custom_match.group(1).strip(),
                            "arg_description": custom_match.group(2).strip(),
                        })
                if "]" in message:
                    refboard_bracflag = False
                    if current_option:
                        current_option["args"][-1]["custom"] = custom_args
                    custom_args = []

            elif "RefBoard:" in message and not refboard_bracflag:
                refboard_description = message.split("RefBoard:", 1)[1].strip()
                refboard_detected, refboard_unbracflag = True, True
                logging.debug(f"Detected RefBoard with description: {refboard_description}")
                if "[" in message or "-" in message:
                    refboard_unbracflag = False
                    if current_option:
                        current_option["args"][-1]["custom"] = custom_args
                    custom_args = []
                if current_option:
                    current_option["args"].append({
                        "arg": "RefBoard",
                        "arg_description": "RefBoard: " + refboard_description,
                        "optional": "No",
                        "custom": custom_args
                    })
                custom_args = []

            elif refboard_unbracflag:
                # Continue processing custom arguments within an unclosed RefBoard block
                if "if custom" in message:
                    custom_match = re.search(r'if custom\s+([\w\[\]:]+)\s*:\s*(.*)', message)
                    if custom_match:
                        custom_args.append({
                            "arg": custom_match.group(1).strip(),
                            "arg_description": custom_match.group(2).strip(),
                        })
                if "[" in message or "-" in message:
                    refboard_unbracflag = False
                    if current_option:
                        current_option["args"][-1]["custom"] = custom_args
                    custom_args = []
                    
                    option_match = re.search(r'\s{1,2}-(?!-)([\w\[\]\(\)\|:\-]+)\s+(.*)', message)
                    if option_match and option_match.group(1) not in seen_options:
                        process_option(current_option)
                        distance = calculate_distance_to_second_word(message) or 2
                        current_option = {
                            "name": option_match.group(1).strip(),
                            "description": option_match.group(2).strip(),
                            "args": []
                        }
                    else:
                        if current_option:
                            arg_match = re.search(r'^\s+([^\s]+(?:\s+[^\s]+)*?)\s{1,}(.*?)(?:\s*\n)?$', message, re.MULTILINE)
                            if arg_match:
                                arg_description = arg_match.group(0)[distance:].strip()
                                selective_value = "Yes" if "[" in arg_match.group(1) else "No"
                                arg = arg_match.group(0)[:distance].strip()
                                cleaned_arg = re.sub(r'[\[\]\(\)]', '', arg)
                                logging.debug(f"Adding argument: {cleaned_arg} with description: {arg_description}")
                                current_option["args"].append({
                                    "arg": cleaned_arg,
                                    "arg_description": arg_description,
                                    "optional": selective_value
                                })
            else:
                # Process messages outside RefBoard blocks
                option_match = re.search(r'\s{1,2}-(?!-)([\w\[\]\(\)\|:\-]+)\s+(.*)', message)
                if option_match and option_match.group(1) not in seen_options:
                    process_option(current_option)
                    distance = calculate_distance_to_second_word(message) or 2
                    current_option = {
                        "name": option_match.group(1).strip(),
                        "description": option_match.group(2).strip(),
                        "args": []
                    }
                else:
                    if current_option:
                        arg_match = re.search(r'^\s+([^\s]+(?:\s+[^\s]+)*?)\s{1,}(.*?)(?:\s*\n)?$', message, re.MULTILINE)
                        if arg_match:
                            arg_description = arg_match.group(0)[distance:].strip()
                            selective_value = "Yes" if "[" in arg_match.group(1) else "No"
                            arg = arg_match.group(0)[:distance].strip()
                            cleaned_arg = re.sub(r'[\[\]\(\)]', '', arg)
                            logging.debug(f"Adding argument: {cleaned_arg} with description: {arg_description}")
                            current_option["args"].append({
                                "arg": cleaned_arg,
                                "arg_description": arg_description,
                                "optional": selective_value
                            })
            logging.debug(f"Option print: {current_option}")

        process_option(current_option)
    logging.debug(f"Total options extracted: {len(options)}")
    return options

def get_file_name(cpp_file_path):
    """
    Determine the file name based on the C++ file path.
    """
    file_names = {
        "EcMasterDemo/EcDemoApp.cpp": "EcMasterDemo",
        "EcMasterDemoDc/EcDemoApp.cpp": "EcMasterDemoDc",
        "EcMasterDemoSyncSm/EcDemoApp.cpp": "EcMasterDemoSyncSm",
        "EcMonitorDemo/EcDemoApp.cpp": "EcMonitorDemo",
        "EcSimulatorHilDemo/EcDemoApp.cpp": "EcSimulatorHilDemo",
        "EcSimulatorSilDemo/EcDemoApp.cpp": "EcSimulatorSilDemo",
        "Common/EcSelectLinkLayer.cpp": "EcSelectLinkLayer",
        "Common/EcDemoParms.cpp": "EcDemoParms"
    }
    return file_names.get(cpp_file_path.split('/')[-2] + '/' + cpp_file_path.split('/')[-1], "Unknown")

def convert_to_json(all_options, output_file):
    """
    Convert the options list to JSON and write it to the specified output file.
    """
    logging.debug(f"Converting options to JSON and writing to {output_file}")
    data = {"Examples": all_options}
    try:
        with open(output_file, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        logging.info(f"Options have been written to {output_file}")
    except IOError as e:
        logging.error(f"Failed to write JSON file: {e}")

def clean_data(d):
    """
    Clean data by removing unnecessary characters.
    """
    if isinstance(d, dict):
        return {k: clean_data(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [clean_data(i) for i in d]
    elif isinstance(d, str):
        return d.replace('\\n', '').replace(']', '')
    return d

def main():
    """
    Main function to process C++ files and generate JSON output.
    """
    parser = argparse.ArgumentParser(description="Extract and convert C++ code options to JSON.")
    parser.add_argument('base_path', help="Base path for the C++ files")
    parser.add_argument('output_json_path', help="Path for the output JSON file")
    args = parser.parse_args()
    
    # List of C++ file paths to process
    cpp_file_paths = [
        f"{args.base_path}Common/EcSelectLinkLayer.cpp",
        f"{args.base_path}Common/EcDemoParms.cpp",
        f"{args.base_path}EcMasterDemo/EcDemoApp.cpp",
        f"{args.base_path}EcMasterDemoDc/EcDemoApp.cpp",
        f"{args.base_path}EcMasterDemoSyncSm/EcDemoApp.cpp",
        f"{args.base_path}EcMonitorDemo/EcDemoApp.cpp",
        f"{args.base_path}EcSimulatorHilDemo/EcDemoApp.cpp",
        f"{args.base_path}EcSimulatorSilDemo/EcDemoApp.cpp"
    ]
    
    all_options = []

    for cpp_file_path in cpp_file_paths:
        logging.debug(f"Processing file: {cpp_file_path}")
        try:
            with open(cpp_file_path, 'r') as cpp_file:
                cpp_code = cpp_file.read()
            options = extract_log_messages_from_function(cpp_code)
            if options:
                file_name = get_file_name(cpp_file_path)
                all_options.append({"example": file_name, "options": options})
        except IOError as e:
            logging.error(f"Failed to read file {cpp_file_path}: {e}")

    if all_options:
        cleaned_options = clean_data(all_options)
        convert_to_json(cleaned_options, args.output_json_path)

if __name__ == "__main__":
    logging.debug("Script started")
    main()
    logging.debug("Script finished")
