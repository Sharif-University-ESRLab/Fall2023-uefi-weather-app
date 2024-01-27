
# Code

This project is part of the Hardware Lab (**CE-40102**) course, featuring a UEFI application designed to display weather information and forecasts for users. The "UEFI Weather APP" directory encompasses the core logic for UEFI interactions and handling HTTP requests, implemented in `C`. In parallel, the "Weather API" directory houses the implementation of a straightforward API that communicates the weather status of a given city to the client, implemented using `Python` (`Django`). Further details on each of these sections are provided below.

## UEFI Weather APP
In this section, we present a high-level overview of our UEFI weather application. Detailed comments are embedded in the code, providing a valuable source for understanding the implementation details. The main code of this project is written in `C`, utilizing libraries provided by **EDK II** for implementation. Additionally, there are extra files in this module for building and informational purposes.

### Main Entry Point (UefiMain)
--------------------
### UefiMain

This function serves as the main entry point for the UEFI application. It orchestrates the entire workflow, including initialization, user input, HTTP communication, data processing, weather report generation, cleanup, and error handling. The code is heavily based on the final example in [UEFI Specification 2022](https://uefi.org/sites/default/files/resources/UEFI_Spec_2_10_Aug29.pdf), version 2.10, section 29.6.

**Parameters:**
- `EFI_HANDLE ImageHandle`: The firmware-allocated handle for the EFI image.
- `EFI_SYSTEM_TABLE *SystemTable`: A pointer to the EFI System Table.

**Returns:** `EFI_SUCCESS` if the entry point is executed successfully; otherwise, an error code.

***Implementation Explanation***

We describe the high-level overview of the implemented code stage by stage.

### Initialization

#### Buffer Allocation

The application starts by allocating a buffer of size `BUFFER_SIZE` (0x100000) to store HTTP response data.

#### Service Binding Protocol

It locates the UEFI HTTP service binding protocol to establish a connection for making HTTP requests.

#### Child Handle Creation

A child handle is created to obtain the HTTP protocol, allowing the application to communicate with HTTP services.

#### HTTP Configuration

The HTTP protocol is configured with parameters such as HTTP version, timeout, and local address settings.

```C++
Status = gBS->AllocatePool(EfiBootServicesData, BUFFER_SIZE, (VOID **)&Buffer);

Status = gBS->LocateProtocol(&gEfiHttpServiceBindingProtocolGuid, NULL, (VOID **)&ServiceBinding);

Status = ServiceBinding->CreateChild(ServiceBinding, &Handle);

Status = gBS->HandleProtocol(Handle, &gEfiHttpProtocolGuid, (VOID **)&Http);

ConfigData.HttpVersion = HttpVersion11;
ConfigData.TimeOutMillisec = 0;
ConfigData.LocalAddressIsIPv6 = FALSE;

ZeroMem(&IPv4Node, sizeof(IPv4Node));
IPv4Node.UseDefaultAddress = TRUE;
IPv4Node.LocalPort = 6349;
ConfigData.AccessPoint.IPv4Node = &IPv4Node;

Status = Http->Configure(Http, &ConfigData);
```

### User Input

The application prompts the user to enter the name of the city (limited to 32 characters) for which they want to retrieve weather information.

### HTTP Request

1. **URL Formation**: The application constructs a URL for the weather API based on the entered city.
2. **Request Initialization**: An HTTP request message is initialized with a GET method and appropriate headers. <ins>*It is important to note that the HTTP request in UEFI will encounter an error if no request header is provided. It is necessary to include at least one header in your request. Most web servers require the inclusion of a `host` header in the input request.*</ins>
3. **Request Token Creation**: A request token is created with an associated event and message.
4. **Request Sending**: The application sends the HTTP request and awaits a callback indicating completion. It also incorporates a timeout mechanism, set to a specific time period (10 seconds in our case).

```C++
RequestData.Url = WeatherURL;
RequestData.Method = HttpMethodGet;
RequestHeaders[0].FieldName = "Host";
RequestHeaders[0].FieldValue = "weather.aghayesefid.ir";
RequestHeaders[1].FieldName = "Auth";
RequestHeaders[1].FieldValue = "Token";
RequestMessage.Data.Request = &RequestData;
RequestMessage.HeaderCount = 2;
RequestMessage.Headers = RequestHeaders;
RequestMessage.BodyLength = 0;
RequestMessage.Body = NULL;

RequestToken.Event = NULL;
Status = gBS->CreateEvent(EVT_NOTIFY_SIGNAL, TPL_CALLBACK, RequestCallback, NULL, &RequestToken.Event);

RequestToken.Status = EFI_SUCCESS;
RequestToken.Message = &RequestMessage;
gRequestCallbackComplete = FALSE;

Status = Http->Request(Http, &RequestToken);

for (Timer = 0; !gRequestCallbackComplete && Timer < 10;) {
    // Poll and timeout logic
}

if (!gRequestCallbackComplete) {
    // Cancel request and go to cleanup
}
```

### HTTP Response Handling

1. **Response Initialization**: An HTTP response message is initialized to receive data.
2. **Response Token Creation**: A response token is created with an associated event and message.
3. **Response Receiving**: The application sends the HTTP response token and waits for the callback.
4. **Chunked Data Download**: In the case of large responses, the application downloads data in chunks until the entire content is received.

```C++
ResponseData.StatusCode = HTTP_STATUS_UNSUPPORTED_STATUS;
ResponseMessage.Data.Response = &ResponseData;
ResponseMessage.HeaderCount = 0;
ResponseMessage.Headers = NULL;
ResponseMessage.BodyLength = BUFFER_SIZE;
ResponseMessage.Body = Buffer;
ResponseToken.Event = NULL;
Status = gBS->CreateEvent(
    EVT_NOTIFY_SIGNAL,
    TPL_CALLBACK,
    ResponseCallback,
    &ResponseToken,
    &ResponseToken.Event
);
ResponseToken.Status = EFI_SUCCESS;
ResponseToken.Message = &ResponseMessage;
gResponseCallbackComplete = FALSE;

Status = Http->Response(Http, &ResponseToken);

for (Timer = 0; !gResponseCallbackComplete && Timer < 10; ) {
    // Poll and timeout logic
}

if (!gResponseCallbackComplete) {
    // Cancel request and go to cleanup
}

for (Index = 0; Index < ResponseMessage.HeaderCount; ++Index) {
    if (!AsciiStriCmp(ResponseMessage.Headers[Index].FieldName, "Content-Length")) {
        ContentLength = AsciiStrDecimalToUintn(ResponseMessage.Headers[Index].FieldValue);
    }
}
ContentDownloaded = ResponseMessage.BodyLength;

while (ContentDownloaded < ContentLength) {
    // Repeat until all chunks of data are downloaded
}
```

### Data Processing

1. **Header Parsing**: The application parses headers to determine the length of the content.
2. **Console Output**: The received data is printed to the UEFI console.

### Weather Report Generation

1. **Data Splitting**: The received data is split into substrings for further processing.
2. **Weather Condition Check**: The application identifies the weather condition from the data.
3. **Displaying Weather Report**: Based on the weather condition, a formatted weather report is displayed on the UEFI console.

### Cleanup

1. **Child Handle Destruction**: The application destroys the child handle and performs cleanup operations.
2. **Memory Deallocation**: Allocated memory, including the city name, Unicode city name, and weather URL, is freed.

```C++
CleanupStatus = ServiceBinding->DestroyChild(ServiceBinding, Handle);
FreePool(CityName);
FreePool(UnicodeCityName);
FreePool(WeatherURL);
```

### Error Handling

The application handles timeouts by canceling requests if no response is received within a specified time. Other errors (like instantiation, allocation, ...) are also handled properly. Error messages are displayed in case of failures, and the program jumps to the cleanup section.

```C++
if (EFI_ERROR(Status)) {
    Print(L"Failed to configure HTTP driver: %r\n", Status);
    goto Cleanup;
}
```


### Request and Response Callbacks
--------------------
#### RequestCallback

This function is invoked when the HTTP request is completed. It sets a global flag (`gRequestCallbackComplete`) to signal the completion of the request.

#### ResponseCallback

Similarly, this function is called upon the completion of the HTTP response. It sets a global flag (`gResponseCallbackComplete`) to indicate that the response has been received.

### Utility Functions
--------------------
#### GetResponseCode

**Purpose:** Translate HTTP status codes to numeric values.

**Parameters:**
- `EFI_HTTP_STATUS_CODE code`: The HTTP status code to be translated.

**Returns:** The numeric representation of the provided HTTP status code.

#### GetInputCityName

**Purpose:** Prompt the user to input the city name.

**Parameters:**
- `CHAR8 *InputString`: The buffer to store the user-entered city name.

**Returns:** `RETURN_SUCCESS` if the input is successful, `RETURN_INVALID_PARAMETER` if the input is empty.

#### SplitString

**Purpose:** Tokenize a string based on a delimiter.

**Parameters:**
- `CHAR8 *InputString`: The string to be tokenized.
- `CHAR8 ***SplitStrings`: A pointer to an array of pointers to tokens.
- `UINT8 *NumTokens`: A pointer to store the number of tokens.

**Returns:** None. Memory for tokens is allocated dynamically.

### Weather Report Display Functions
--------------------
#### PrintClearWeatherReport, PrintCloudsWeatherReport, ...

Each of these functions is responsible for displaying weather reports based on the specific weather condition. They format and print relevant information like temperature, humidity, wind speed, and description to the UEFI console.

**Parameters:**
- `CHAR8 **WeatherReport`: An array of strings containing weather information.

**Returns:** None.

### WeatherApplication.dsc File 
-----
This .dsc file configures the build settings for our application. It includes definitions for platform details, architecture support, build targets, and various libraries required for different stages of UEFI execution (PEI Core, DXE Core, DXE Driver, Runtime Driver, SMM Core, DXE SMM Driver, UEFI Driver, UEFI Application). The file organizes these configurations under specific sections, providing a structured setup for building the UEFI Weather Application. For more information about each of these concepts, you can visit **EDK II** documentation.

### WeatherApplication.inf File
------
This .inf file configures the details of the UEFI Weather Application module. It provides information such as module version, entry point, source files, required packages, library classes, GUIDs, protocols, PCDs, and other settings needed for building and integrating the application into the UEFI firmware. For more information about each of these concepts, you can visit **EDK II** documentation.

### WeatherApplication.uni File
-------
This .uni file contains string definitions for the UEFI Weather Application module. It provides abstract and descriptive information about the module for localization purposes.

## Weather API

This is a straightforward web server implemented in `Python`, leveraging the `Django` framework, serving as an intermediary for our Weather App. The UEFI application dispatches a customized request to this server. Subsequently, the web server initiates the required API calls and processes the request, ultimately sending a simplified response back to the application. This approach reduces the need for extensive `C` code to interact with APIs, enhancing the program's maintainability and portability, with only a marginal sacrifice in performance. Below, you'll find a high-level documentation of critical components of this API, highlighting its key logic.

### demo/views.py File
--------
This `Django` view serves as the API for the UEFI application, fetching weather information based on user-provided location data.

### Functions

#### **get_weather_to_status(weather_info)**

This function processes weather information and returns a simplified status. It checks for mist-related conditions and returns 'mist' if detected; otherwise, it returns the primary weather status.

#### **get_weather_by_geo_location(lat, lon)**

Fetches weather information based on geographical coordinates (latitude and longitude). It utilizes the OpenWeatherMap API and returns a formatted string containing temperature, wind speed, humidity, weather status, and description.

#### **get_geo_location(location_name)**

Obtains geographical coordinates (latitude and longitude) based on a location name using the Mapbox API. Returns a dictionary containing latitude, longitude, and location name.

#### **get_weather_by_location_name(location_name)**

Combines the functionality of `get_geo_location` and `get_weather_by_geo_location` to fetch weather information based on a location name.

### Class: **DemoAPIView**

This class inherits from the `APIView` class provided by the Django Rest Framework.

#### HTTP GET Request Handling

Handles HTTP GET requests to fetch weather information.

##### Request Headers

- **Auth**: Should contain the user API token for authentication.

##### Query Parameters

- **location**: Specifies the location for which weather information is requested.

#### Response

- If authentication fails, returns a 401 Unauthorized response.
- If there is an issue fetching weather information, returns a 500 Internal Server Error response.
- Otherwise, returns a 200 OK response with the fetched weather information.

#### Usage

Make a GET request to this API endpoint with the required headers and query parameters to retrieve weather information.

Example:

```http
GET /weather?location=NewYork
Auth: <USER_API_TOKEN>
```

Response:
```text
"23.55.2,75,clouds,Scattered Clouds"
```

### Build & Run
--------
There are some **Dockerfiles** and a **docker-compose** file that can easily build and run the webserver. It uses **Nginx** to serve requests.

Run this command on your shell to build and run the weather API:

```shell
docker-compose up -d
```
