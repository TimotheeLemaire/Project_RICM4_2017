

class NameSet : 
        self.names
        self.mutex

        def __init__(self): 
                self.names = Hash::new
                self.mutex = Mutex::new
        

        def get_name(name)
                string = nil
                @mutex.synchronize {
                        if @names[name] then
                                @names[name] += 1
                                string = name + @names[name].to_s
                        else
                                string = name
                                @names[name] = 1
                        end
                }
                return string
        end

end