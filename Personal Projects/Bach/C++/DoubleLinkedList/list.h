#ifndef DDLIST_H
#define DDLIST_H

#include <vector>
#include <stdexcept>
#include <iostream>

template <typename T>
/**
 * @brief A representation of an element in the List.
 * 
 */
struct Node
{
    T data;
    Node<T>* next;
    Node<T>* prev;

    Node() { next = nullptr; prev = nullptr; }
    Node(T const& data) 
    {
        next = nullptr; 
        prev = nullptr; 
        this->data = data; 
    }
};

template <typename T>
/**
 * @brief A representation of a double linked list.
 * 
 * This list is low-level, meaning you can do whatever with the list, and you'll face consequence for that.
 * 
 */
class List
{
private:
    /**
     * @brief Pointer to the first element of the list.
     * 
     */
    Node<T>* head;
    /**
     * @brief Pointer to the last element of the list.
     * 
     */
    Node<T>* tail;
    /**
     * @brief The size of the list.
     * 
     */
    unsigned int len;
public:
    /**
     * @brief The public pointer to the list.
     * 
     * This pointer is recommended to point to the head at all time.
     * It can be used to modify directly any data in the list.
     * However, it is recommended to use `operator[]` to access the element in the list than this pointer.
     * 
     * This pointer should be used to traverse the list.
     * 
     */
    Node<T>* iter;

    List() { head = nullptr; tail = nullptr; iter = nullptr; len = 0; }
    ~List()
    {
        clear();
    }
    /**
     * @brief Return pointer to the first element.
     * 
     * @return __Node<T>*__ Pointer to the first element.
     * 
     * @see back()
     * 
     */
    Node<T>* front() { return head; }
    /**
     * @brief Return pointer to the last element.
     * 
     * @return __Node<T>*__ Pointer to the last element.
     * 
     * @see front()
     * 
     */
    Node<T>* back() { return tail; }

    /**
     * @brief A check if the container is empty.
     * 
     * @return __bool__
     * 
     * @see size()
     * 
     */
    bool empty() { return (len == 0); }
    /**
     * @brief Return the size of the list.
     * 
     * @return __unsigned int__ The size of the list.
     * 
     * @see back()
     * 
     */
    unsigned int size() { return len; }

    /**
     * @brief Construct and insert the element at the back.
     * 
     * @param data The data to construct.
     * 
     * @exception std::bad_alloc If there's not enough allocated memory.
     * 
     * @see push_back(Node<T>* element)
     * @see push_front(T const& data)
     * @see push_front(Node<T>* element)
     * 
     */
    void push_back(T const& data)
    {
        Node<T>* element = new Node<T>(data);
        if (len > 0)
        {
            tail->next = element;
            element->prev = tail;
            tail = element;
        }
        else
        {
            head = element;
            tail = element;
        }
        len++;
    }
    /**
     * @brief Insert the element at the back.
     * 
     * @param element The pointer to the element to insert.
     * 
     * @see push_back(T const& data)
     * @see push_front(T const& data)
     * @see push_front(Node<T>* element)
     * 
     */
    void push_back(Node<T>* element)
    {
        if (len > 0)
        {
            tail->next = element;
            element->prev = tail;
            tail = element;
        }
        else
        {
            head = element;
            tail = element;
        }
        len++;
    }
    /**
     * @brief Construct and insert the element at the front.
     * 
     * @param data The data to construct.
     * 
     * @exception std::bad_alloc If there's not enough allocated memory.
     * 
     * @see push_front(Node<T>* element)
     * @see push_back(Node<T>* element)
     * @see push_back(T const& data)
     * 
     */
    void push_front(T const& data)
    {
        Node<T>* element = new Node<T>(data);
        if (len == 0)
        {
            head = element;
            tail = element;
        }
        else
        {
            head->prev = element;
            element->next = head;
            head = element;
        }
        len++;
    }
    /**
     * @brief Insert the element at the front.
     * 
     * @param element The pointer to the element to insert.
     * 
     * @see push_front(T const& data)
     * @see push_back(Node<T>* element)
     * @see push_back(T const& data)
     * 
     */
    void push_front(Node<T>* element)
    {
        if (len == 0)
        {
            head = element;
            tail = element;
        }
        else
        {
            head->prev = element;
            element->next = head;
            head = element;
        }
        len++;
    }
    /**
     * @brief Remove the last element, return the pointer to it.
     * 
     * It is a heap allocated element, therefore, you can delete the pointer if it's not longer used in a list.
     * 
     * @return __Node<T>*__ The pointer to the removed Node. `nullptr` if the size is 0.
     * 
     * @see pop_front()
     * 
     */
    Node<T>* pop_back()
    {
        Node<T>* element = tail;
        if (len > 1)
        {
            tail->prev->next = nullptr;
            tail = tail->prev;
            element->prev = nullptr;
        }
        else if (len == 0) element = nullptr;

        len--;
        return element;
    }
    /**
     * @brief Remove the first element, return the pointer to it.
     * 
     * It is a heap allocated element, therefore, you can delete the pointer if it's not longer used in a list.
     * 
     * @return __Node<T>*__ The pointer to the removed Node. `nullptr` if the size is 0.
     * 
     * @see pop_back()
     * 
     */
    Node<T>* pop_front()
    {
        Node<T>* element = head;
        if (len > 1)
        {
            head->next->prev = nullptr;
            head = head->next;
            element->next = nullptr;
        }
        else if (len == 0) element = nullptr;

        len--;
        return element;
    }
    /**
     * @brief Construct and insert an element before pos.
     * 
     * @param data The data to construct.
     * @param pos The pointer to an element to insert before, `nullptr` if insert at the back.
     * 
     * @exception std::bad_alloc If there's not enough memory to allocate.
     * 
     * @see insert(Node<T>* element, Node<T>* pos)
     * @see remove(Node<T>* pos)
     * 
     */
    void insert(T const& data, Node<T>* pos)
    {
        if (pos == nullptr) push_back(data);
        else if (pos == head) push_front(data);
        else
        {
            Node<T>* element = new Node<T>(data);
            pos->prev->next = element;
            element->prev = pos->prev;
            pos->prev = element;
            element->next = pos;
            len++;
        }
    }
    /**
     * @brief Insert an element before pos.
     * 
     * @param element The pointer to the element to insert.
     * @param pos The pointer to an element to insert before, `nullptr` if insert at the back.
     * 
     * @see insert(T const& data, Node<T>* pos)
     * @see remove(Note<T>* pos)
     * 
     */
    void insert(Node<T>* element, Node<T>* pos)
    {
        if (pos == head)
            push_front(element);
        else if (pos == nullptr) 
            push_back(element);
        else
        {
            pos->prev->next = element;
            element->prev = pos->prev;
            pos->prev = element;
            element->next = pos;
        }
    }
    /**
     * @brief Remove the element, return the pointer to it.
     * 
     * It is a heap allocated element, therefore, you can delete the pointer if it's not longer used in a list.
     *
     * @param pos The pointer to the element to remove. 
     * @return __Node<T>*__ The pointer to the removed Node. `nullptr` if the size is 0.
     * 
     * @see insert(Node<T>* element, Node<T>* pos)
     * 
     */
    Node<T>* remove(Node<T>* pos)
    {
        if (pos == tail) 
            return pop_back();
        else if (pos == head)
            return pop_front();
        else
        {
            Node<T>* element = pos;
            pos->next->prev = pos->prev;
            pos->prev->next = pos->next;
            pos->next = nullptr;
            pos->prev = nullptr;
            len--;
            return element;
        }
    }
    /**
     * @brief Move an element to a destination. Note that it insert *before* the `pos`.
     * 
     * @param element Pointer to the element you want to insert.
     * @param pos Pointer to the location you want to insert.
     * 
     * @note If element is not belong to the list, the behavior is *undefined*.
     * @note If element is nullptr, the behavior is *undefined*.
     * 
     * @see swap(Node<T>& first, Node<T>& second)
     * 
     */
    void moveto(Node<T>* element, Node<T>* pos)
    {
        if (pos != nullptr)
        {
            if (element == pos->prev) 
                return;
            if (element == pos->next)
            {
                if (pos != head)
                    pos->prev->next = element;
                else
                    head = element;
                
                element->prev = pos->prev;
                if (element != tail)
                    element->next->prev = pos;
                else
                    tail = pos;
                
                pos->next = element->next;
                element->next = pos;
                pos->prev = element;

                return;
            }
        }
        if (pos == head)
        {
            element->prev->next = element->next;
            if (element != tail)
                element->next->prev = element->prev;
            else
                tail = element->prev;
            
            element->prev = nullptr;
            element->next = head;
            head->prev = element;
            head = element;
        }
        else if (pos == nullptr)
        {
            element->next->prev = element->prev;
            if (element != head)
                element->prev->next = element->next;
            else
                head = element->next;
            
            element->next = nullptr;
            element->prev = tail;
            tail->next = element;
            tail = element;
        }
        else
        {
            if (element == head)
            {
                element->next->prev = nullptr;
                head = element->next;
            }
            else if (element == tail)
            {
                element->prev->next = nullptr;
                tail = element->prev;
            }
            else 
            {
                element->prev->next = element->next;
                element->next->prev = element->prev;
            }
            element->next = pos;
            element->prev = pos->prev;
            pos->prev->next = element;
            pos->prev = element;
        }
        
    }
    /**
     * @brief Clear every elements in the list.
     * 
     * Any references, pointers to the element will be *invalidated*.
     * The `iter` from the list will also be *invalidated*.
     * 
     */
    void clear()
    {
        iter = head;
        int counter = 0;
        if (len == 0) return;
        while (iter->next != nullptr)
        {
            iter = head->next;
            delete head;
            //std::cout << counter++ << std::endl;
            head = iter;
        }
        len = 0;
        delete iter;
    }
    /**
     * @brief Access the element at the position.
     * 
     * Treat this as the array accessing operator. It is a "safe" `iter` version of accessing element.
     * 
     * Please note that if the list is corrupted, this method will result in *undefined behavior*.
     * 
     * @param index The position of the element.
     * @return __Node<T>&__ The reference to the element.
     * 
     */
    Node<T>& operator[](int const& index)
    {
        iter = head;
        int count = 0;
        while (count != index)
        {
            iter = iter->next;
            count++;
        }
        return *iter;
    }
    /**
     * @brief Swap the two elements.
     * 
     * Internally, this swap the pointers rather than the data itself. Therefore, it is highly unstable and a messed up means the list is corrupted.
     * 
     * This method is still in testing process.
     * 
     * @param first The element to swap.
     * @param second The element to swap.
     * 
     * @see iswap(Node<T>& first, Node<T>& second)
     * 
     */
    void swap(Node<T>& first, Node<T>& second)
    {
        if (len <= 1) return;
        if (first.next == &second)
            moveto(&second, &first);
        else if (second.next == &first)
            moveto(&first, &second);
        else
        {
            Node<T>* temp = first.next;
            moveto(&first, second.next);
            moveto(&second, temp);
        }
    }
    /**
     * @brief Swap the two elements.
     * 
     * Internally, this swap the data itself rather than the pointer. Therefore, it is recommended to use this in small data type only.
     * 
     * @param first The element to swap.
     * @param second The element to swap.
     * 
     * @see swap(Node<T>& first, Node<T>& second)
     * 
     */
    void iswap(Node<T>& first, Node<T>& second)
    {
        T temp = first.data;
        first.data = second.data;
        second.data = temp;
    }
    void print()
    {
        if (len == 0) return;
        iter = head;
        std::cout << "Size: " << len << std::endl;
        int realsize = 0;
        while (iter->next != nullptr)
        {
            std::cout << "My address: " << iter << std::endl;
            std::cout << "|" << iter->prev << "|";
            std::cout << "|" << &(iter->data) << "|";
            std::cout << "|" << iter->next << "|";
            std::cout << std::endl;
            iter = iter->next;
            realsize++;
        }
        std::cout << "My address: " << iter << std::endl;
        std::cout << "|" << iter->prev << "|";
        std::cout << "|" << &(iter->data) << "|";
        std::cout << "|" << iter->next << "|";
        std::cout << std::endl;
        std::cout << "Current head: " << head << std::endl;
        std::cout << "Current tail: " << tail << std::endl;
        std::cout << "Real Size: " << ++realsize << std::endl;
        iter = head;
    }
};

#endif