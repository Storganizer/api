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
erDiagram
    LOCATION ||--o{ BOX : places
    LOCATION {
        string name
        string description
        string image
    }
    BOX ||--|{ ITEM : contains
    BOX {
        int orderNumber
        string deliveryAddress
    }
    ITEM {
        string productCode
        int quantity
        float pricePerUnit
    }
```
