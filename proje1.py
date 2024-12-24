from tabulate import tabulate

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []  # Alt düğümleri saklar

    def add_child(self, child):
        self.children.append(child)

    def collect_data(self, level=0):
        """Veriyi tablo formatı için toplar."""
        data = [["  " * level + self.name]]
        for child in self.children:
            data.extend(child.collect_data(level + 1))
        return data

class Graph:
    def __init__(self):
        self.adjacency_list = {}  # Grafın komşuluk listesi temsili

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, from_vertex, to_vertex):
        if from_vertex in self.adjacency_list and to_vertex in self.adjacency_list:
            self.adjacency_list[from_vertex].append(to_vertex)
            self.adjacency_list[to_vertex].append(from_vertex)  # İki yönlü bağlantı

class ShiftSchedule:
    def __init__(self):
        # Günler ve vardiya saatlerini saklamak için bir ağaç yapısı
        self.root = TreeNode("Vardiya Planı")
        self.days = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        self.shifts = ["09:00-17:00", "17:00-01:00"]

        # Ağaç yapısını oluştur
        for day in self.days:
            day_node = TreeNode(day)
            for shift in self.shifts:
                shift_node = TreeNode(shift)
                day_node.add_child(shift_node)
            self.root.add_child(day_node)

        # Graf yapısı
        self.graph = Graph()
        for day in self.days:
            self.graph.add_vertex(day)

    def assign_shifts(self, shift_assignments):
        """Kullanıcıdan alınan vardiya atamalarına göre çalışanları ağaç yapısına ekler."""
        for day_index, day_node in enumerate(self.root.children):  # Gün düğümleri
            for shift_index, shift_node in enumerate(day_node.children):  # Vardiya düğümleri
                assigned_employees = shift_assignments[day_index][shift_index]
                if len(assigned_employees) > 8:
                    raise ValueError(f"Hata: {day_node.name} - {shift_node.name} vardiyasına 8'den fazla çalışan atanamaz.")
                for employee in assigned_employees:
                    shift_node.add_child(TreeNode(employee))

                # Graf yapısına çalışanları ekle
                for i in range(len(assigned_employees)):
                    self.graph.add_vertex(assigned_employees[i])
                    for j in range(i + 1, len(assigned_employees)):
                        self.graph.add_edge(assigned_employees[i], assigned_employees[j])

    def display_schedule(self):
        """Vardiya planını tablo formatında ekrana yazdırır."""
        data = []
        for day_node in self.root.children:
            for shift_node in day_node.children:
                employees = [child.name for child in shift_node.children]
                data.append([day_node.name, shift_node.name, ", ".join(employees)])
        headers = ["Gün", "Vardiya", "Çalışanlar"]
        print(tabulate(data, headers=headers, tablefmt="grid"))

# Kullanıcı girdileri
employees = ["Mehmet", "Eren", "İbrahim", "Halil", "Selman", "Selin", "Esra", "Hande"]

# Kullanıcıdan vardiya atamalarını alma
shift_assignments = []
for day in ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]:
    day_assignments = []
    for shift in ["09:00-17:00", "17:00-01:00"]:
        while True:
            assigned_employees = input(f"Lütfen {day} günü için {shift} vardiyasında çalışacak çalışanları giriniz (virgülle ayırarak): ").split(",")
            assigned_employees = [employee.strip() for employee in assigned_employees]
            if len(assigned_employees) > 8:
                print("Hata: 8 çalışanınız var. Bir vardiyaya 8'den fazla çalışan atanamaz. Tekrar deneyiniz.")
            elif not all(employee in employees for employee in assigned_employees):
                print("Hata: Girilen çalışanlardan en az biri mevcut çalışan listesinde değil. Tekrar deneyiniz.")
            else:
                break
        day_assignments.append(assigned_employees)
    shift_assignments.append(day_assignments)

# Proje çalışması
schedule = ShiftSchedule()
schedule.assign_shifts(shift_assignments)
schedule.display_schedule()

