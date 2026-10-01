import os
from .helper import CONFIG_DATA

def ask_date(prompt):
    while True:
        val = input(prompt).strip()
        if not val: return val
        if len(val) == 8 and val.isdigit():
            day, month, year = int(val[:2]), int(val[2:4]), int(val[4:])
            if (1 <= day <= 31) and (1 <= month <= 12) and (1900 <= year <= 2027):
                return val
            print("[-] Error: Invalid date (Day:01-31, Month:01-12, Year:1900-2027).")
        else:
            print("[-] Error: Exactly 8 digits required (e.g., 19032007).")

def ask_list(prompt):
    while True:
        val = input(prompt).strip().lower()
        if not val: return []
        if " " in val and "," not in val:
            print("[-] Error: Separate multiple items with commas (e.g., hacker,cyber,2026).")
            continue
        return [m for m in [word.replace(" ", "") for word in val.split(',')] if m]

def ask_text(prompt):
    return input(prompt).strip().lower().replace(" ", "")

def ask_yes_no(prompt):
    while True:
        val = input(prompt + " (Y/N): ").strip().upper()
        if val in ['Y', 'YES']: return True
        if val in ['N', 'NO', '']: return False

def interactive_mode():
    print("\n[!] Leave blank and press ENTER to skip any question.")
    info = {}
    
    # Primary information
    info['firstname'] = ask_text("> Target's First Name: ")
    info['lastname'] = ask_text("> Target's Last Name: ")
    info['nickname'] = ask_text("> Target's Nickname: ")
    info['dob'] = ask_date("> Date of Birth (DDMMYYYY): ")
    
    # Context and entourage
    info['partner_firstname'] = ask_text("> Partner's First Name: ")
    info['partner_lastname'] = ask_text("> Partner's Last Name: ")
    info['partner_dob'] = ask_date("> Partner's Date of Birth (DDMMYYYY): ")
    info['pet'] = ask_text("> Pet's Name: ")
    info['company'] = ask_text("> Company or School: ")
    
    info['cities'] = ask_list("> City/Cities (format: city1,city2): ")
    info['keywords'] = ask_list("> Additional keywords (hobbies, etc.): ")
    
    print("\n[!] Mutation Engine Configuration")
    info['opt_special'] = ask_yes_no("> Append special characters to words?")
    info['opt_numbers'] = ask_yes_no("> Append random numbers (0-100) to words?")
    info['opt_leet'] = ask_yes_no("> Enable Leet Speak mode (e.g., a=@, e=3)?")
    
    return info

def extract_base_words(info):
    base = []
    fields = ['firstname', 'lastname', 'nickname', 'partner_firstname', 'partner_lastname', 'pet', 'company']
    for field in fields:
        if info.get(field): base.append(info[field])
    base.extend(info['cities'])
    base.extend(info['keywords'])
    return [word for word in base if word]

def generate_mutations(info):
    passwords = set()
    base_words = extract_base_words(info)
    
    years = list(CONFIG_DATA.years)
    if info['dob']: years.append(info['dob'][4:])
    if info['partner_dob']: years.append(info['partner_dob'][4:])

    # 1. Base (lowercase, capitalized)
    for word in base_words:
        passwords.add(word.lower())
        passwords.add(word.capitalize())
        
    # 2. Raw dates
    if info['dob']: passwords.add(info['dob'])
    if info['partner_dob']: passwords.add(info['partner_dob'])

    # 3. Combinations (Firstname + Lastname)
    if info['firstname'] and info['lastname']:
        passwords.add(f"{info['firstname']}{info['lastname']}")
        passwords.add(f"{info['firstname'].capitalize()}{info['lastname'].capitalize()}")

    current_words = list(passwords)
    
    # 4. Append years and special characters
    for word in current_words:
        for year in years:
            passwords.add(f"{word}{year}")
            if info['opt_special']:
                for char in CONFIG_DATA.special_chars:
                    passwords.add(f"{word}{year}{char}")
                    passwords.add(f"{word}{char}{year}")
        
        if info['opt_special']:
            for char in CONFIG_DATA.special_chars:
                passwords.add(f"{word}{char}")

    # 5. Append numbers (0 to 100)
    if info['opt_numbers']:
        temp_set = set()
        for word in passwords:
            for i in range(101):
                temp_set.add(f"{word}{i}")
        passwords.update(temp_set)

    # 6. Leet Speak
    if info['opt_leet']:
        leet_passwords = set()
        for word in passwords:
            leet_word = word
            for char, sub in CONFIG_DATA.leet.items():
                leet_word = leet_word.replace(char, sub)
            if leet_word != word:
                leet_passwords.add(leet_word)
        passwords.update(leet_passwords)
        
    return passwords

def save_dictionary(passwords, firstname):
    filename = f"{firstname if firstname else 'target'}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for pwd in sorted(passwords):
            f.write(pwd + '\n')
    size_kb = os.path.getsize(filename) / 1024
    print(f"\n {len(passwords):,} passwords successfully generated in {filename} ({size_kb:.2f} KB)".replace(',', ' '))