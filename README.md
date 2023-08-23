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
    LOCATION {
        string name
        string description
        string image
    }
    LOCATION ||--|{ BOX : stores

    
    BOX {
        string name
        string description
    }
    BOX ||--|{ ITEM : contains


    ITEM {
        string name
        int quantity
        float pricePerUnit
    }
    ITEM }|--|{ TAG : has

    TAG {
        string name
        string value
    }
```
