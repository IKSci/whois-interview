from bs4 import BeautifulSoup
import requests


def parse_nested_info(element):
    nested_info = {}
    lines = element.get_text(separator='\n', strip=True).split('\n')
    for i in range(0, len(lines), 2):
        key = lines[i].replace(':', '').strip()
        value = lines[i+1].strip() if (i+1) < len(lines) else ''
        nested_info[key] = value
    return nested_info

def extract_whois_table(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    table = soup.find('table')
    table_dict = {}

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 2:
            key = cells[0].get_text(strip=True).replace('\n', ' ').strip(':')
            if key in ["Регистрант", "Административныйконтакт"]:
                nested_dict = parse_nested_info(cells[1])
                table_dict[key] = nested_dict
            elif key == "Серверы имен":
                value = []
                current_entry = ""
                for element in cells[1].children:
                    if element.name == 'a' and element.find('b'):
                        if current_entry:
                            value.append(current_entry.strip())
                        current_entry = element.find('b').get_text(strip=True) + " "
                    elif element.name == 'b':
                        current_entry += element.get_text(strip=True) + " "
                if current_entry:
                    value.append(current_entry.strip())
                table_dict[key] = ', '.join(value)
            elif key == "Дата окончания":
                value = cells[1].get_text(separator=' ', strip=True).replace('\n', ' ')
                remaining_days = cells[1].find('b', class_='text-danger')
                if remaining_days:
                    value += f" {remaining_days.get_text(strip=True)}"
                table_dict[key] = value
            else:
                value = cells[1].get_text(separator=' ', strip=True).replace('\n', ' ')
                table_dict[key] = value

    return table_dict


def extract_whois_text(html):
    soup = BeautifulSoup(html.content, 'html.parser')
    pre_tag = soup.find('pre')

    if not pre_tag:
        return None

    lines = pre_tag.get_text().split('\n')
    whois_data = {}
    current_key = None
    for line in lines:
        line = line.strip()
        if line.startswith(">>> Last update of WHOIS database:"):
            break

        if ": " in line:
            key, value = line.split(": ", 1)
            whois_data[key.strip()] = value.strip()
            current_key = key.strip()
        else:
            if current_key:
                whois_data[current_key] += f" {line.strip()}"

    return whois_data

def get_dictionary(domain):
    url = "https://www.ps.kz/domains/whois/result?q="
    response = requests.get(url + domain)
    soup = BeautifulSoup(response.content, 'html.parser')
    result = {}
    result['domain_name'] = domain
    
    busy_div = soup.find('div', class_="domains-whois__result domains-whois--busy")
    result_div = soup.find('div', class_="domains-whois__result")
    
    if busy_div:
        result['status'] = "busy"
        if soup.find("pre", style="background-color: white; border: none; box-shadow: 0 10px 6px -6px rgba(0,0,0,.4);"):
            whois_data = extract_whois_text(response)
            result['details'] = {"reason": "Domain is already registered.", "whois_data": whois_data}
        
        else:            
            subtitle_text = busy_div.get_text(strip=True)
            if "Возникли непредвиденные проблемы" in subtitle_text:
                result['details'] = {"reason": "Unexpected problems occurred"}
                
                return result
            elif "К сожалению, покупка домена" in subtitle_text:
                result['details'] = {"reason": "Domain purchase is not available"}
                
                return result
            whois_data = extract_whois_table(response)
            if whois_data:
                result['details'] = {"reason": "Domain is already registered.", "whois_data": whois_data}
            else:
                result['details'] = {"reason": "Domain is already registered."}
    elif result_div:
        result['status'] = "available"
        result['details'] = {"reason": "Domain is available for registration"}
        return result
    else:
        result['status'] = "unknown"
        result['details'] = {"reason": "Unknown status"}
        return result

    return result