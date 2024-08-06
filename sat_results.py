import json

class SATResults:
    def __init__(self, filename: str = "sat_results.json"):
        self.filename = filename
        self.records = self.load_data()
    
    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.records, f, indent=4)
    
    def insert_data(self, name, address, city, country, pincode, sat_score):
        passed = "Pass" if sat_score > 30 else "Fail"
        record = {
            "Name": name,
            "Address": address,
            "City": city,
            "Country": country,
            "Pincode": pincode,
            "SAT Score": sat_score,
            "Passed": passed
        }
        self.records.append(record)
        self.save_data()
    
    def view_all_data(self):
        return self.records
    
    def get_rank(self, name):
        sorted_records = sorted(self.records, key=lambda x: x["SAT Score"], reverse=True)
        for rank, record in enumerate(sorted_records, start=1):
            if record["Name"] == name:
                return rank
        return -1
    
    def update_score(self, name, new_score):
        for record in self.records:
            if record["Name"] == name:
                record["SAT Score"] = new_score
                record["Passed"] = "Pass" if new_score > 30 else "Fail"
                self.save_data()
                return True
        return False
    
    def delete_one_record(self, name):
        for i, record in enumerate(self.records):
            if record["Name"] == name:
                del self.records[i]
                self.save_data()
                return True
        return False
    
    def calculate_average_score(self):
        if not self.records:
            return 0.0
        total_score = sum(record["SAT Score"] for record in self.records)
        return total_score / len(self.records)
    
    def filter_by_pass_fail(self, status):
        return [record for record in self.records if record["Passed"] == status]

def menu():
    manager = SATResults()

    while True:
        print("\nSAT Results Manager")
        print("1. Insert data")
        print("2. View all data")
        print("3. Get rank")
        print("4. Update score")
        print("5. Delete one record")
        print("6. Calculate Average SAT Score")
        print("7. Filter records by Pass/Fail Status")
        print("8. Exit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            name = input("Name: ")
            address = input("Address: ")
            city = input("City: ")
            country = input("Country: ")
            pincode = input("Pincode: ")
            sat_score = int(input("SAT Score: "))
            manager.insert_data(name, address, city, country, pincode, sat_score)
            print("Data inserted successfully.")
        
        elif choice == "2":
            data = manager.view_all_data()
            print(json.dumps(data, indent=4))
        
        elif choice == "3":
            name = input("Enter name to get rank: ")
            rank = manager.get_rank(name)
            if rank != -1:
                print(f"Rank of {name} is {rank}.")
            else:
                print("Name not found.")
        
        elif choice == "4":
            name = input("Enter name to update score: ")
            new_score = int(input("New SAT Score: "))
            if manager.update_score(name, new_score):
                print("Score updated successfully.")
            else:
                print("Name not found.")
        
        elif choice == "5":
            name = input("Enter name to delete: ")
            if manager.delete_one_record(name):
                print("Record deleted successfully.")
            else:
                print("Name not found.")
        
        elif choice == "6":
            average_score = manager.calculate_average_score()
            print(f"Average SAT Score: {average_score:.2f}")
        
        elif choice == "7":
            status = input("Enter status (Pass/Fail) to filter: ")
            filtered_records = manager.filter_by_pass_fail(status)
            print(json.dumps(filtered_records, indent=4))
        
        elif choice == "8":
            break
        
        else:
            print("Invalid option. Please try again.")

# Call the menu function to run the program
menu()
