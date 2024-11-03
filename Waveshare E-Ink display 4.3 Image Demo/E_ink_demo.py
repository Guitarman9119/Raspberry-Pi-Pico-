import utime
from logo import youtube_logo


from e_ink_library import EPD_4in2_B

EPD_WIDTH = 400
EPD_HEIGHT = 300

if __name__ == '__main__':
    epd = EPD_4in2_B()
    
    
    # Display the YouTube logo 
    logo_width = 400
    logo_height = 300

    # Calculate the starting point to center the logo
    start_x = (EPD_WIDTH - logo_width) // 2
    start_y = (EPD_HEIGHT - logo_height) // 2

    for y in range(logo_height):
        for x in range(logo_width):
            if youtube_logo[y * (logo_width // 8) + (x // 8)] & (128 >> (x % 8)):
                epd.imageblack.pixel(start_x + x, start_y + y, 0xff)  
    
    epd.EPD_4IN2B_Display(epd.buffer_black)
    epd.delay_ms(5000)  
    epd.Sleep()