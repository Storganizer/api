# storganizer
Application to manage your storage at home



## High Level Architecture

```mermaid
  graph TD;
    Database-->Api;
    Api-->Database;

    Api<-->Website;

    Api<-->MobileApp;

```

## Data Structure


```mermaid
  graph TD;
    Location;
    Box;
    Item;

    Location-->Box;
    Box-->Item;

```

```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER {
        string name
        string custNumber
        string sector
    }
    ORDER ||--|{ LINE-ITEM : contains
    ORDER {
        int orderNumber
        string deliveryAddress
    }
    LINE-ITEM {
        string productCode
        int quantity
        float pricePerUnit
    }
```
