TARGET = buildingok

.PHONY: default all clean

default: $(TARGET)
all: default


%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

.PRECIOUS: $(TARGET) $(OBJECTS)

$(TARGET):
	go build -o buildingok .

clean:
	-rm -f *.o
	-rm -f $(TARGET)
	-rm -f vgcore*
