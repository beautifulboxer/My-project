#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Student {
    char name[50], roll[20], pass[20];
};

struct StudentNode {
    struct Student s;
    struct StudentNode *left, *right;
};

struct RequestNode {
    char name[50], roll[20], hostel[20], room[20], occ[20], wash[20], status[20];
    struct RequestNode* next;
};

struct ReviewNode {
    char roll[20], comment[200];
    int mess, laundry, playground, water, wifi, gym;
    struct ReviewNode* next;
};

struct ReviewNode* reviews = NULL;

void clearInputBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

void readLine(char *b, int n) {
    fgets(b, n, stdin);
    int l = strlen(b);
    if (l > 0 && b[l-1] == '\n') b[l-1] = '\0';
}

struct StudentNode* newStudentNode(struct Student s) {
    struct StudentNode* n = malloc(sizeof(struct StudentNode));
    n->s = s; n->left = n->right = NULL;
    return n;
}

struct StudentNode* addStudent(struct StudentNode* r, struct Student s) {
    if (!r) return newStudentNode(s);
    if (strcmp(s.roll, r->s.roll) < 0) r->left = addStudent(r->left, s);
    else if (strcmp(s.roll, r->s.roll) > 0) r->right = addStudent(r->right, s);
    return r;
}

struct StudentNode* findStudent(struct StudentNode* r, char* roll) {
    if (!r) return NULL;
    if (strcmp(roll, r->s.roll) == 0) return r;
    return strcmp(roll, r->s.roll) < 0 ? findStudent(r->left, roll) : findStudent(r->right, roll);
}

struct RequestNode* addReq(struct RequestNode* h, struct RequestNode* r) {
    r->next = NULL;
    if (!h) return r;
    struct RequestNode* t = h;
    while (t->next) t = t->next;
    t->next = r;
    return h;
}

struct RequestNode* makeRequest(struct Student s) {
    struct RequestNode* r = malloc(sizeof(struct RequestNode));
    strcpy(r->name, s.name); strcpy(r->roll, s.roll);
    
    int ch;
    printf("\n=== Hostel Request Form ===\n");
    printf("Hostel Type (1-In Campus / 2-Out Campus): "); scanf("%d", &ch);
    strcpy(r->hostel, ch == 1 ? "In" : "Out");
    printf("Room Type (1-AC / 2-Non AC): "); scanf("%d", &ch);
    strcpy(r->room, ch == 1 ? "AC" : "Non-AC");
    printf("Occupancy (1-Single / 2-Double / 3-Triple): "); scanf("%d", &ch);
    strcpy(r->occ, ch == 1 ? "Single" : ch == 2 ? "Double" : "Triple");
    printf("Washroom (1-With / 2-Without): "); scanf("%d", &ch);
    strcpy(r->wash, ch == 1 ? "With" : "Without");
    
    strcpy(r->status, "Pending");
    printf("\nRequest submitted successfully!\n");
    return r;
}

void showRequests(struct RequestNode* h) {
    printf("\n=== All Hostel Requests ===\n");
    if (!h) { printf("No requests found.\n"); return; }
    
    int count = 1;
    while (h) {
        printf("\nRequest #%d:\nName: %s\nRoll: %s\n", count++, h->name, h->roll);
        printf("Hostel: %s | Room: %s\nOccupancy: %s | Washroom: %s\nStatus: %s\n", 
               h->hostel, h->room, h->occ, h->wash, h->status);
        printf("------------------------\n");
        h = h->next;
    }
}

void manageRequests(struct RequestNode* h) {
    printf("\n=== Manage Requests ===\n");
    if (!h) { printf("No requests found.\n"); return; }
    
    struct RequestNode* current = h;
    int found = 0;
    
    while (current) {
        if (strcmp(current->status, "Pending") == 0) {
            found = 1;
            printf("\nPending Request from %s (Roll: %s)\n", current->name, current->roll);
            printf("Hostel: %s | Room: %s | Occupancy: %s | Washroom: %s\n", 
                   current->hostel, current->room, current->occ, current->wash);
            
            printf("Action: 1-Approve, 2-Reject: ");
            int choice; scanf("%d", &choice);
            
            if (choice == 1) { strcpy(current->status, "Approved"); printf("Request approved!\n"); }
            else if (choice == 2) { strcpy(current->status, "Rejected"); printf("Request rejected!\n"); }
            else printf("Invalid choice! Request skipped.\n");
        }
        current = current->next;
    }
    if (!found) printf("No pending requests found.\n");
}

void checkStatus(struct RequestNode* h, char* roll) {
    printf("\n=== Check Request Status ===\n");
    while (h) {
        if (strcmp(h->roll, roll) == 0) {
            printf("\nRequest Details:\nName: %s\nHostel: %s\nRoom: %s\n", h->name, h->hostel, h->room);
            printf("Occupancy: %s\nWashroom: %s\nStatus: %s\n", h->occ, h->wash, h->status);
            return;
        }
        h = h->next;
    }
    printf("No request found for this roll number.\n");
}

void submitReview(char* roll) {
    printf("\n=== Submit Review ===\n");
    struct ReviewNode* r = malloc(sizeof(struct ReviewNode));
    strcpy(r->roll, roll);

    printf("Rate the following facilities (1-5):\n");
    printf("Mess Service: "); scanf("%d", &r->mess);
    printf("Laundry Service: "); scanf("%d", &r->laundry);
    printf("Playground: "); scanf("%d", &r->playground);
    printf("Water Services: "); scanf("%d", &r->water);
    printf("WiFi: "); scanf("%d", &r->wifi);
    printf("Gym: "); scanf("%d", &r->gym);

    clearInputBuffer();
    printf("Comments: "); readLine(r->comment, 200);

    r->next = NULL;
    if (!reviews) reviews = r;
    else {
        struct ReviewNode* t = reviews;
        while (t->next) t = t->next;
        t->next = r;
    }
    printf("Review submitted successfully!\n");
}

void showReviews() {
    printf("\n=== Student Reviews ===\n");
    if (!reviews) { printf("No reviews available.\n"); return; }

    struct ReviewNode* t = reviews;
    int count = 1;
    while (t) {
        printf("\nReview #%d\nRatings - Mess:%d Laundry:%d Playground:%d Water:%d WiFi:%d Gym:%d\n",
               count++, t->mess, t->laundry, t->playground, t->water, t->wifi, t->gym);
        printf("Comment: %s\n------------------------\n", t->comment);
        t = t->next;
    }
}

int adminLogin() {
    printf("\n=== Admin Login ===\n");
    char username[20], password[20];
    printf("Username: "); scanf("%s", username);
    printf("Password: "); scanf("%s", password);
    
    if (strcmp(username, "admin") == 0 && strcmp(password, "admin123") == 0) {
        printf("Login successful!\n"); return 1;
    }
    printf("Invalid credentials!\n"); return 0;
}

void waitForEnter() {
    printf("\nPress Enter to continue...");
    clearInputBuffer(); getchar();
}

void showMainMenu() {
    printf("\n========== HOSTEL MANAGEMENT SYSTEM ==========\n");
    printf("1. Admin Login\n2. Student Portal\n3. Exit\n");
    printf("==============================================\nChoose an option: ");
}

void showAdminMenu() {
    printf("\n========== ADMIN DASHBOARD ==========\n");
    printf("1. Manage Requests\n2. View All Requests\n3. View Reviews\n4. Back to Main Menu\n");
    printf("====================================\nChoose an option: ");
}

void showStudentMenu() {
    printf("\n========== STUDENT PORTAL ==========\n");
    printf("1. Register\n2. Login\n3. Check Request Status\n4. Back to Main Menu\n");
    printf("===================================\nChoose an option: ");
}

void showStudentDashboard() {
    printf("\n========== STUDENT DASHBOARD ==========\n");
    printf("1. Submit Hostel Request\n2. Submit Review\n3. Logout\n");
    printf("======================================\nChoose an option: ");
}

int main() {
    struct StudentNode* bst = NULL;
    struct RequestNode* reqs = NULL;
    int mainChoice, adminChoice, studentChoice, dashboardChoice;
    
    printf("Welcome to Hostel Management System!\n");
    
    while(1) {
        showMainMenu(); scanf("%d", &mainChoice); clearInputBuffer();

        if (mainChoice == 1) {
            if (adminLogin()) {
                do {
                    showAdminMenu(); scanf("%d", &adminChoice); clearInputBuffer();
                    switch(adminChoice) {
                        case 1: manageRequests(reqs); break;
                        case 2: showRequests(reqs); break;
                        case 3: showReviews(); break;
                        case 4: printf("Returning to main menu...\n"); break;
                        default: printf("Invalid choice!\n");
                    }
                    if (adminChoice != 4) waitForEnter();
                } while (adminChoice != 4);
            } else waitForEnter();
        }
        else if (mainChoice == 2) {
            do {
                showStudentMenu(); scanf("%d", &studentChoice); clearInputBuffer();

                if (studentChoice == 1) {
                    struct Student st;
                    printf("\n=== Student Registration ===\nFull Name: "); readLine(st.name, 50);
                    printf("Roll Number: "); scanf("%s", st.roll); clearInputBuffer();

                    if (findStudent(bst, st.roll)) {
                        printf("This roll number is already registered!\n"); waitForEnter(); continue;
                    }
                    printf("Password: "); scanf("%s", st.pass); clearInputBuffer();
                    bst = addStudent(bst, st); printf("Registration successful! You can now login.\n"); waitForEnter();
                }
                else if (studentChoice == 2) {
                    char roll[20], password[20];
                    printf("\n=== Student Login ===\nRoll Number: "); scanf("%s", roll);
                    printf("Password: "); scanf("%s", password); clearInputBuffer();

                    struct StudentNode* student = findStudent(bst, roll);
                    if (!student || strcmp(password, student->s.pass) != 0) {
                        printf("Invalid credentials!\n"); waitForEnter(); continue;
                    }
                    printf("Login successful! Welcome, %s!\n", student->s.name);
                    
                    do {
                        showStudentDashboard(); scanf("%d", &dashboardChoice); clearInputBuffer();
                        if (dashboardChoice == 1) {
                            struct RequestNode* temp = reqs; int requestExists = 0;
                            while (temp) {
                                if (strcmp(temp->roll, student->s.roll) == 0) {
                                    printf("You have already submitted a request!\n"); requestExists = 1; break;
                                } temp = temp->next;
                            }
                            if (!requestExists) reqs = addReq(reqs, makeRequest(student->s));
                            waitForEnter();
                        }
                        else if (dashboardChoice == 2) { submitReview(student->s.roll); waitForEnter(); }
                        else if (dashboardChoice == 3) printf("Logging out...\n");
                        else printf("Invalid choice!\n");
                    } while (dashboardChoice != 3);
                }
                else if (studentChoice == 3) {
                    char roll[20]; printf("Enter Roll Number to check status: "); scanf("%s", roll); clearInputBuffer();
                    checkStatus(reqs, roll); waitForEnter();
                }
                else if (studentChoice == 4) printf("Returning to main menu...\n");
                else printf("Invalid choice!\n");
            } while (studentChoice != 4);
        }
        else if (mainChoice == 3) { printf("\nThank you for using Hostel Management System!\n"); break; }
        else printf("Invalid choice! Please try again.\n");
    }
    return 0;
}