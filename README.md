# storganizer
Application to manage your storage at home

```mermaid
  graph TD;
      Database-->Api;
      Api-->Database;

      Api-->Website;
      Website-->Api;
      
      Api-->MobileApp;
      MobileApp-->Api;

```