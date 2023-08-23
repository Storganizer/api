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

    Brand {
        string name
    }




    LOCATION ||--|{ BOX : stores
    BOX ||--|{ ITEM : contains
    ITEM }|--|{ TAG : has
    ITEM ||--|{ BRAND : is



```
