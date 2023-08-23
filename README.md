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

    
    BOX {
        string name
        string description
    }


    ITEM {
        string name
        string description
        string image

    }

    TAG {
        string name
        string value
    }

    BRAND {
        string name
    }




    LOCATION ||--|{ BOX : stores
    BOX ||--|{ ITEM : contains
    ITEM }|--|{ TAG : has
    ITEM }|--|| BRAND : is



```


## Planned Features
- QR Codes or NFC Tags on boxes to check what is in there
- QR Codes or NFC Tags to identify an object
- Search function for items by brand, tags, fulltext search to identify an object
- Possibility to find identified objects or check where there belong to 